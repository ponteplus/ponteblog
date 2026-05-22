---
title: Bem-vindo ao blog PontePlus
date: 2026-05-21T10:00:00-03:00
slug: bem-vindo-ao-blog-ponteplus
tags:
  - ponteplus
  - blog
draft: false
authors:
  - PontePlus
summary: Por que separamos o blog editorial da plataforma e como publicar novos artigos.
---

Este é o primeiro post do **blog estático** da PontePlus.

## Por que um blog separado?

A plataforma PontePlus já oferece blog integrado para cada profissional (posts no painel, publicados no site do cliente). O conteúdo **da empresa** — novidades do produto, tutoriais gerais, SEO para liberais — fica mais simples de manter assim:

- Arquivos **Markdown** versionados no Git
- Site **estático** (sem banco, sem deploy de API)
- Build automático no push (GitHub Actions → GitHub Pages ou Netlify)

Inspirado no fluxo descrito por [Fabio Akita](https://akitaonrails.com/2025/09/10/meu-novo-blog-como-eu-fiz/) com Hugo e Hextra.

## Como escrever um novo artigo

1. Crie `content/blog/meu-artigo.md` (ou copie o [archetype](archetypes/blog.md))
2. Preencha o front matter (`title`, `date`, `slug`, `tags`, `summary`)
3. Preview local: `make serve`
4. Commit e push na branch `main`

## Próximos passos

- Apontar `blog.ponteplus.com.br` para o deploy
- Linkar o blog na landing em [ponteplus.com.br](https://ponteplus.com.br)
- Publicar artigos sobre onboarding, SEO e cases de clientes

Obrigado por ler — **just write**.
