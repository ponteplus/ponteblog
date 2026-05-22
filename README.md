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
| Um repo por marca (`ponteplus/ponteblog`) | ✅ |
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
| `.github/workflows/pages.yaml` — deploy em push na `main` | ✅ |
| `.github/workflows/ci.yaml` — build em PRs (sem publicar) | ✅ |
| `static/CNAME` + `.nojekyll` para Pages | ✅ |
| Repositório remoto + Pages + DNS `blog.ponteplus.com.br` | ⏳ configurar no GitHub (passos abaixo) |

### Fase 5 — Integração com o produto ⏳

| Item | Status |
|------|--------|
| Decisão editorial no repositório | ✅ |
| Link **Blog** na landing `ponteplus.com.br` → `https://blog.ponteplus.com.br` | ⏳ fora deste repo |

## Licença

MIT — ver [LICENSE](LICENSE).
