PKGNAME := jaraco-starter
VERSION ?= 0.1.0
TARBALL := $(PKGNAME)-$(VERSION).tar.gz

dist:
	mkdir -p dist
	tar --exclude=dist -czf dist/$(TARBALL) .

abuild: dist
	cp dist/$(TARBALL) .
	abuild -r

install-sample:
	mkdir -p $(HOME)/.config/jaraco
	cp starter.sample.json $(HOME)/.config/jaraco/starter.json
