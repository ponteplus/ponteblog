# PontePlus Blog

Blog estático da **PontePlus** — artigos em Markdown, gerados com [Hugo](https://gohugo.io/) + [Hextra](https://imfing.github.io/hextra/).

## Pré-requisitos

- [Hugo Extended](https://gohugo.io/installation/) (≥ 0.156)
- [Go](https://go.dev/dl/) (módulos Hugo)
- Git

## Desenvolvimento local

```bash
make setup   # hugo mod tidy (baixa o tema Hextra)
make serve   # http://localhost:1313
```

## Novo artigo

```bash
make new SLUG=meu-artigo TITLE="Título do artigo"
```

Cria `content/blog/<YYYY>/<MM>/<slug>.md` (organização em pastas; URL continua `/blog/<slug>/`). No front matter, use `authors: [renan-rodrigues]` (slugs em `data/authors.yaml`).

## Estrutura

```
content/
  _index.md              # Home (posts por ano-mês via shortcode)
  about.md               # Sobre
  blog/
    _index.md            # Listagem /blog
    <YYYY>/<MM>/*.md     # Posts (path físico; URL sem data)
  archives/_index.md     # Arquivo cronológico (ano → mês)
  authors/               # Perfis da equipe (/authors/<slug>/)
data/
  authors.yaml           # Cadastro de autores (nome, links, papel)
layouts/                 # Overrides (home, arquivo, autores, TL;DR…)
assets/css/custom.css    # Cores Ponte+
archetypes/blog.md
hugo.yaml
```

URLs dos posts: `/blog/<slug>/` (sem ano/mês no path).

## Status por fase

### Fase 1 — Decisões ✅

| Item | Status |
|------|--------|
| Stack Hugo Extended + Hextra (`go.mod`, `make setup`) | ✅ |
| Um repo por marca (`pontedev/ponteblog`) | ✅ |
| Domínio planejado `https://blog.ponteplus.com.br/` em `hugo.yaml` | ✅ |
| Blog SaaS dos clientes **não** migra para cá (só editorial da marca) | ✅ documentado |

### Fase 2 — Repositório e site base ✅

| Item | Status |
|------|--------|
| Páginas: `content/_index.md`, `about.md`, `blog/`, `archives/` | ✅ |
| URLs `/blog/<slug>/` (`permalinks` em `hugo.yaml`) | ✅ |
| Posts em `content/blog/<YYYY>/<MM>/` (organização local) | ✅ |
| Menus: Blog, **Equipe**, Sobre, Site PontePlus, Contato, Busca, **Tema** | ✅ |
| Posts publicados: ex. `hello-world` (`draft: false`) | ✅ |
| Makefile: `setup`, `serve`, `build`, `new`, `clean` | ✅ |
| Tema claro/escuro + cores Ponte+ (`assets/css/custom.css`) | ✅ |
| Home estilo [AkitaOnRails](https://github.com/akitaonrails/akitaonrails.github.io): posts por **ano → mês** com âncoras | ✅ (`{{% blog-by-month %}}`) |
| Regras Cursor (`.cursor/rules/`) | ✅ |

### Fase 3 — Conteúdo e automação ✅ (parcial em imagens)

| Item | Status |
|------|--------|
| Front matter no archetype: `title`, `date`, `slug`, `tags`, `draft`, `authors`, `summary` | ✅ |
| Listagem `/blog/` com tags, data e **byline de autor** | ✅ |
| Arquivo `/archives/` agrupado **ano → mês** | ✅ (`layouts/archives.html`) |
| Taxonomia **autores** + `/authors/` e `/authors/<slug>/` | ✅ (`data/authors.yaml`) |
| RSS + sitemap (Hugo → `public/index.xml`, `sitemap.xml`) | ✅ |
| TL;DR ChatGPT no topo de cada post | ✅ (`layouts/_partials/custom/tldr-link.html`; `tldr: false` para desligar) |
| Script Ruby `generate_index` | ❌ não necessário (Hugo + shortcode) |
| Imagens S3/R2 + convenção no repo | ⏳ pendente |

### Fase 4 — Deploy e DNS ⏳

| Item | Status |
|------|--------|
| `.github/workflows/pages.yaml` — deploy em push na `main` | ✅ primário |
| `.github/workflows/ci.yaml` — build em PRs (sem publicar) | ✅ |
| `static/CNAME` + `.nojekyll` para Pages | ✅ |
| `netlify.toml` | ✅ opcional (segundo plano) |
| Repositório remoto + Pages + DNS `blog.ponteplus.com.br` | ⏳ configurar no GitHub (passos abaixo) |

### Fase 5 — Integração com o produto ⏳

| Item | Status |
|------|--------|
| Decisão editorial no repositório | ✅ |
| Link **Blog** na landing `ponteplus.com.br` → `https://blog.ponteplus.com.br` | ⏳ fora deste repo |

## Tema claro / escuro e cores

- **Alternar tema:** rodapé ou menu mobile → Claro / Escuro / Sistema (`hugo.yaml` → `params.theme`).
- **Cores Ponte+ (roxo `#7B5EA7`, fundo claro):** `assets/css/custom.css` — ver [Customizing Hextra](https://imfing.github.io/hextra/docs/advanced/customization/).
- Após mudar CSS: reinicie `make serve` e use hard refresh (Ctrl+Shift+R).

## Deploy (GitHub Pages — primário)

### CI/CD no repositório

| Workflow | Quando roda | O que faz |
|----------|-------------|-----------|
| [`.github/workflows/ci.yaml`](.github/workflows/ci.yaml) | PR → `main` | `hugo mod tidy` + build; falha se `public/index.html` ou sitemap não existirem |
| [`.github/workflows/pages.yaml`](.github/workflows/pages.yaml) | Push → `main` | Build com `baseURL` do Pages + deploy em **github-pages** |

Hugo **0.161.1** Extended no CI (alinhado ao `go.mod`). Cache de módulos Go/Hugo entre runs.

### Publicar pela primeira vez

1. **Criar o repo no GitHub** (ex. `ponteplus/ponteblog`) e enviar a branch `main`:
   ```bash
   git remote add origin git@github.com:ORG/ponteblog.git
   git push -u origin main
   ```
2. No GitHub: **Settings → Pages**
   - **Build and deployment → Source:** `GitHub Actions` (não “Deploy from branch”).
3. Após o primeiro push, abra **Actions** → workflow **Deploy PontePlus Blog** e confira se passou (build + deploy).
4. **Domínio customizado** (opcional mas recomendado):
   - **Settings → Pages → Custom domain:** `blog.ponteplus.com.br`
   - No DNS do domínio (Registro.br, Cloudflare, etc.):
     - Tipo **CNAME**, nome `blog`, valor `<usuario-ou-org>.github.io` (o GitHub mostra o alvo exato na tela de Pages).
   - Aguarde verificação e marque **Enforce HTTPS**.
   - O arquivo [`static/CNAME`](static/CNAME) já declara `blog.ponteplus.com.br` no artefato publicado.
5. Confirme `baseURL` em [`hugo.yaml`](hugo.yaml): `https://blog.ponteplus.com.br/` (já definido).

URL padrão antes do CNAME: `https://<org>.github.io/<repo>/` — o workflow usa o `base_url` que o Pages injeta no build para links relativos corretos.

### Proteção de branch (recomendado)

Em **Settings → Branches → Branch protection rules** para `main`:

- Exigir PR antes de merge (opcional para time pequeno).
- **Require status checks:** `build` (workflow **CI**) — assim PRs só entram se o Hugo compilar.

### Netlify (segundo plano)

[`netlify.toml`](netlify.toml) permanece como alternativa (preview ou host extra). **Não** é necessário se só usar GitHub Pages. Se conectar o repo na Netlify, use o mesmo comando de build; o deploy primário continua sendo o Actions acima.

## Domínio sugerido

| Uso | Host |
|-----|------|
| Blog | `blog.ponteplus.com.br` |
| Plataforma / landing | `ponteplus.com.br` |

## Licença

MIT — ver [LICENSE](LICENSE).
