---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
slug: {{ .File.ContentBaseName }}
tags: []
draft: true
authors:
  - renan-rodrigues  # slug em data/authors.yaml (renan-rodrigues | niverton-felipe | samuel-agra)
summary:
---

Resumo em uma frase (aparece na listagem).

Conteúdo do artigo em Markdown.
