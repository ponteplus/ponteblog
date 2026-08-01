---
title: Da VPS “segura” ao HTTPS que não quer nascer (saga de deploy)
date: 2026-08-01T10:00:00-03:00
slug: ponteplus-vps-hostinger-saga
tags:
  - deploy
  - vps
  - infra
  - docker
draft: false
authors:
  - renan-rodrigues
summary: SSH ok, UFW ligado, docker compose “Succeeded” — e o site ainda mostrando página parked do registrador. A saga completa.
---

Beleza. SSH ok, usuário com sudo, UFW ligado, backup semanal ativado no painel. Você tá se sentindo DevOps.

Agora falta só “subir a aplicação”.

Só isso. Quatro palavrinhas. Várias horas.

Este post é a saga inteira: do VPS zerado até o `curl` devolver JSON no endpoint de health — com os erros que aparecem quando você faz na ordem “errada mas humana”, e o que de fato precisa estar certo: usuário, chave, firewall, Docker, `.env`, banco gerenciado, DNS, reverse proxy e o certificado que se recusa a nascer porque a pasta de log do proxy não existe.

Spoiler: o `docker compose up` “Succeeded” e o site continua mostrando página parked do registrador. Vida.

---

## 0. Não inventa painel agora

Vai ter vontade de meter Dokploy / Coolify / “alguma UI linda”.

Nesta stack o edge é **reverse proxy no host** (Caddy, nginx ou similar) + TLS + app em loopback. Painel genérico compete com isso e vira outro projeto.

Fica no SO limpo (Plain OS). Depois, se quiser painel, usa pra *outro* app.

---

## 1. VPS — o chão de fábrica

Colocar um projeto no ar começa antes do `docker compose up`. Nesta etapa você deixa o VPS limpo, com um usuário próprio, acesso por chave SSH e um firewall mínimo.

No painel do provedor, escolha um **VPS** (não hospedagem compartilhada). Para um SaaS pequeno com Docker + proxy + banco externo, um plano intermediário costuma bastar no início.

| Item | Valor |
|---|---|
| Tipo | VPS |
| Local | Região próxima aos usuários (ex. Brasil) |
| SO | **Plain OS — Ubuntu LTS recente** |
| Painel | Sem cPanel / painéis pesados — SO limpo |

**Por que Plain OS?** Painéis extras consomem RAM e complicam a topologia. O proxy fica no host e a app em containers; quanto menos “mágica” no meio, melhor.

Crie o VPS, anote o **IP público** e a senha root. No dashboard, abra o terminal e, como root:

```bash
apt update && apt upgrade -y
```

### Usuário (e parar de viver como root)

O `root` pode tudo. Um typo, um script malicioso ou um comando colado da internet com privilégio total pode destruir o servidor. Trabalhe com usuário comum + `sudo`.

```bash
adduser username
usermod -aG sudo username
su - username
```

### Chave SSH

No **PC local**:

```bash
ssh-keygen -t ed25519 -C "vps-deploy"
cat ~/.ssh/id_ed25519.pub
```

No VPS, como o usuário novo:

```bash
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys   # cola a .pub, uma linha
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Teste do PC:

```bash
ssh username@IP_DO_VPS
```

### Firewall (UFW) — ordem importa

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

Regra mental: **SSH primeiro, depois web, depois enable.** Backend/Docker ficam em loopback (`127.0.0.1`); a internet só fala com 80/443 via proxy — por isso não abrimos portas da API/frontend no UFW.

No painel do provedor: **backup** + **scan de malware** se existir — camada extra no host, não substitui backup do banco.

---

## 2. Docker — o erro clássico do “package has no installation candidate”

Você cola o `apt install docker-ce ...` e o Ubuntu responde, educado:

> Package docker-ce is not available

Porque o Ubuntu **não** vende `docker-ce` no apt padrão. Precisa do repo da Docker primeiro ([docs oficiais](https://docs.docker.com/engine/install/ubuntu/)):

```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Depois:

```bash
sudo usermod -aG docker $USER
# sai e entra no SSH de novo, senão continua “permission denied” no socket
```

Confirma:

```bash
docker --version
docker compose version
sudo docker run --rm hello-world
```

---

## 3. Proxy no host (oficial, não o pacote zumbi do Ubuntu)

Mesma lógica do Docker: use o install **oficial** do proxy que você escolheu (ex. [Caddy](https://caddyserver.com/docs/install)).

`apt install` sem o repo do projeto = versão atrasada e surpresa no config.

Ordem boa: instalar o proxy **agora**, mas só aplicar o config de produção **depois** da app estar healthy no loopback. Senão o TLS fica falhando contra um backend morto.

---

## 4. Pasta do app — `/opt` e o misterioso `containerd`

```bash
sudo mkdir -p /opt/nome-do-app
sudo chown SEU_USER:SEU_USER /opt/nome-do-app
```

`chown` no `/opt` inteiro funciona, mas é grosso. Prefira só a pasta do projeto.

Depois do Docker, pode aparecer `/opt/containerd`. Não é vírus. É o runtime. `Permission denied` nela = normal. Ignore e vá pra pasta do app.

---

## 5. O compose certo (sim, existe o errado)

```bash
# DEV — compose local, banco em container ou local
docker compose -f docker-compose.yml up -d --build

# PROD na VPS — arquivo de compose de produção do projeto
docker compose -f docker-compose.prod.yml up -d --build
```

Se aparecer `permission denied ... docker.sock`: ou `sudo`, ou você esqueceu de relogar depois do grupo `docker`.

Confere status e health no loopback (porta e path vêm do seu compose):

```bash
docker compose -f docker-compose.prod.yml ps
curl -s http://127.0.0.1:PORTA_API/health
```

`Started` ≠ healthy. Se o curl voltar vazio, olha log do serviço da API:

```bash
sudo docker compose -f docker-compose.prod.yml logs --tail=80 NOME_SERVICO_API
```

---

## 6. Tour pelos erros do banco (coleção de figurinhas)

| Erro no log | Tradução humana |
|---|---|
| `Authentication failed` | Usuário/senha da URI errados. Ou senha com caracteres especiais sem URL-encode. |
| `SSL handshake failed` | Rede/TLS. Quase sempre **IP da VPS fora da allowlist** do banco gerenciado. |
| `DuplicateKeyError` em tenant/slug | Você mudou o domínio e o seed tentou recriar dados que já existiam. |

IP da VPS:

```bash
curl -4 ifconfig.me
```

No painel do banco → Network Access → libera **só o IP da VPS**. Evite abrir para `0.0.0.0/0` em produção.

Se o seed quebrar após mudar domínio, ajuste o registro existente no banco em vez de recriar do zero — o procedimento depende do seu schema; não execute updates aleatórios em produção sem backup.

Depois:

```bash
sudo docker compose -f docker-compose.prod.yml up -d --force-recreate NOME_SERVICO_API
curl -s http://127.0.0.1:PORTA_API/health
```

Frontend healthy e API unhealthy = site “sobe” e backend não. Adivinha qual página você testa primeiro.

---

## 7. DNS — “eu juro que configurei” vs página parked

No painel do domínio:

| Tipo | Nome | Valor |
|---|---|---|
| A | `@` | IP da VPS |
| CNAME | `www` | `app.exemplo.com` |

Confere **na VPS**:

```bash
curl -4 ifconfig.me
dig +short app.exemplo.com A
```

Os dois iguais? Bom.

`curl https://app.exemplo.com/health` devolvendo HTML de “domínio parked”? DNS ainda não aponta pra VPS (ou cache/propagação). Não adianta xingar o proxy ainda.

---

## 8. Config do proxy — o domínio que você tem, não o do README

O runbook interno pode citar outro domínio. O config do proxy precisa bater com o domínio **que você comprou e apontou no DNS**:

```text
app.exemplo.com, www.app.exemplo.com {
    reverse_proxy 127.0.0.1:PORTA_FRONTEND
}
```

Pasta de log do proxy (exemplo com Caddy — ajuste se usar nginx):

```bash
sudo mkdir -p /var/log/caddy
sudo chown caddy:caddy /var/log/caddy   # isso aqui salvou o deploy. anota.

sudo cp /opt/nome-do-app/path/ao/config-de-producao /etc/caddy/Caddyfile
# edita os hosts se precisar
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

App só em loopback (portas da API e do frontend no compose). Internet fala com 80/443 no proxy. UFW já liberou isso no começo — se não liberou, boa sorte debugando “timeout” pra sempre.

**Não publique** o config completo nem paths internos do repo em posts públicos — basta o padrão (reverse proxy → loopback).

---

## 9. ERR_SSL_PROTOCOL_ERROR — o vilão era pasta de log

Sintomas de quem já passou por isso:

- `dig` aponta pro IP certo
- `ss` mostra o proxy em `:80` e `:443`
- HTTP responde redirect para HTTPS
- HTTPS: alerta TLS / browser `ERR_SSL_PROTOCOL_ERROR`

Journal do proxy:

```text
challenge failed … acme-challenge/… : 500
```

Tradução: Let's Encrypt bateu no challenge e o proxy devolveu **500**.

No nosso caso, log em arquivo sem diretório/permissão correta.

```bash
sudo mkdir -p /var/log/caddy
sudo chown caddy:caddy /var/log/caddy
sudo systemctl restart caddy
curl -vk --max-time 30 https://app.exemplo.com/health
```

Quando der certo, o browser mostra certificado válido e o health retorna JSON — não precisa publicar o payload completo.

O `unable to get local issuer certificate` no curl da VPS às vezes é CA store local — o browser costuma ficar ok. Se o browser também reclamar, aí sim investiga.

---

## 10. Frontend: o detalhe que o `.env` não resolve sozinho

O frontend em produção costuma ter **domínio ou host da plataforma** fixo no build (config/i18n), não só no `.env`.

Mudou o domínio? Ajusta essa config, rebuilda o container do frontend, senão a app “não se reconhece” como host certo mesmo com HTTPS lindo.

```bash
cd /opt/nome-do-app
# depois do git pull com o domínio certo:
sudo docker compose -f docker-compose.prod.yml up -d --build NOME_SERVICO_FRONTEND
```

---

## Checklist final (sem romantizar)

**Host (antes do compose):**

- [ ] VPS, SO limpo, updates aplicados
- [ ] Usuário + grupo `sudo`; chave SSH; `ssh username@IP` ok
- [ ] UFW: OpenSSH + 80 + 443, enable
- [ ] Backup no provedor + scan de malware se disponível

**Deploy:**

- [ ] Docker + grupo `docker` (relogin)
- [ ] Proxy instalado (repo oficial)
- [ ] Compose de **produção** (não o de dev)
- [ ] Banco: URI ok + **só** IP da VPS na allowlist
- [ ] Tenant/domínio alinhado com o que a app espera
- [ ] DNS A/`www` → IP da VPS (`dig` confere)
- [ ] Config do proxy com esse domínio + pasta de log writable
- [ ] `https://SEU_DOMINIO/health` → JSON healthy
- [ ] Browser abre o site; login admin com credenciais fortes (não as de exemplo)
- [ ] Domínio no frontend alinhado + rebuild



---

## Epílogo

No papel, a saga é: VPS segura → Docker → clone → `.env` → compose → DNS → proxy → HTTPS.

Na prática é uma sequência de “me ajuda com o error” até o health devolver JSON e a página parked sumir.

Se algo quebrar de novo: log da API, journal do proxy, `dig` e `curl -vk`. Nessa ordem.

E não, `Started` no compose não significa que o mundo está bem.
