PKGNAME := jaraco-starter
VERSION ?= 0.1.0
TARBALL := $(PKGNAME)-$(VERSION).tar.gz

.PHONY: dist abuild install-sample

dist:
	mkdir -p dist
	LC_ALL=C tar \
		--exclude=dist \
		--sort=name \
		--mtime='UTC 2024-01-01' \
		--owner=0 \
		--group=0 \
		--numeric-owner \
		-cf - . | gzip -n > dist/$(TARBALL)

abuild: dist
	cp dist/$(TARBALL) .
	abuild -r

install-sample:
	mkdir -p $(HOME)/.config/jaraco
	cp starter.sample.json $(HOME)/.config/jaraco/starter.json
