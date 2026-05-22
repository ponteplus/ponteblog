.PHONY: setup serve build new clean

HUGO ?= hugo
PORT ?= 1313

setup:
	$(HUGO) mod tidy

serve: setup
	$(HUGO) server --buildDrafts --disableFastRender -p $(PORT)

build: setup
	$(HUGO) --gc --minify

new:
	@test -n "$(SLUG)" || (echo "Uso: make new SLUG=meu-artigo TITLE='Título opcional'"; exit 1)
	$(HUGO) new blog/$(SLUG).md --kind blog
	@if [ -n "$(TITLE)" ]; then \
		sed -i 's/^title: .*/title: $(TITLE)/' content/blog/$(SLUG).md; \
	fi
	@echo "Criado: content/blog/$(SLUG).md"

clean:
	rm -rf public resources _vendor
