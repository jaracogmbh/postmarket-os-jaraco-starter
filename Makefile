PKGNAME := jaraco-starter
VERSION ?= 0.1.0
TARBALL := $(PKGNAME)-$(VERSION).tar.gz
RELEASE_FILES := \
	LICENSE \
	Makefile \
	README.md \
	pyproject.toml \
	setup.py \
	starter.sample.json \
	data/io.jaraco.Starter.desktop \
	data/io.jaraco.Starter.metainfo.xml \
	data/io.jaraco.Starter.policy \
	data/io.jaraco.Starter.svg \
	src/jaraco_starter/__init__.py \
	src/jaraco_starter/runner.py \
	tests/test_runner.py

.PHONY: dist abuild install-sample

dist:
	mkdir -p dist
	LC_ALL=C tar \
		--sort=name \
		--mtime='UTC 2024-01-01' \
		--owner=0 \
		--group=0 \
		--numeric-owner \
		--mode=0644 \
		-cf - $(RELEASE_FILES) | gzip -n > dist/$(TARBALL)

abuild: dist
	cp dist/$(TARBALL) .
	abuild -r

install-sample:
	mkdir -p $(HOME)/.config/jaraco
	cp starter.sample.json $(HOME)/.config/jaraco/starter.json
