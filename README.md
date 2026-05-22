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

Isso cria `content/blog/meu-artigo.md` a partir do archetype. Edite o arquivo, rode `make serve` e confira no navegador.

## Estrutura

```
content/
  _index.md          # Home
  about.md           # Sobre
  blog/
    _index.md        # Listagem /blog
    *.md             # Posts
  archives/
    _index.md        # Arquivo cronológico
archetypes/
  blog.md            # Template de post
hugo.yaml            # Configuração
```

URLs dos posts: `/blog/<slug>/` (sem ano/mês no path).

## Deploy

### GitHub Pages

Workflow em `.github/workflows/pages.yaml` — push em `main` publica o site.

1. Crie o repositório remoto (ex. `ponteplus/ponteplus-blog`)
2. `git remote add origin … && git push -u origin main`
3. Em **Settings → Pages**, fonte: **GitHub Actions**
4. Ajuste `baseURL` em `hugo.yaml` para a URL final (ex. `https://blog.ponteplus.com.br/`)

### Netlify

`netlify.toml` já configurado. Conecte o repo e defina o domínio customizado.

## Domínio sugerido

| Uso | Host |
|-----|------|
| Blog | `blog.ponteplus.com.br` |
| Plataforma / landing | `ponteplus.com.br` |

## Licença

MIT — ver [LICENSE](LICENSE).
