PY?=python3
PELICAN?=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

GITHUB_PAGES_BRANCH=gh-pages


DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

SERVER ?= "0.0.0.0"

PORT ?= 0
ifneq ($(PORT), 0)
	PELICANOPTS += -p $(PORT)
endif

.PHONY: help
help:
	@echo 'Makefile for seth.fischer.nz                                              '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          serve and regenerate together      '
	@echo '   make github                         upload the web site via gh-pages   '
	@echo '   make install-git-hooks              install Git hooks                  '
	@echo '   make install-ide-config             install IDE configuration          '
	@echo '   make install-vale-styles            install Vale styles                '
	@echo '   make lint                           run all linters                    '
	@echo '   make lint-prose                     lint prose                         '
	@echo '   make test-links-internal            test internal HTML links           '
	@echo '   make test-links-prod                test production HTML links         '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

.PHONY: html
html:
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

.PHONY: clean
clean:
	[ ! -d "$(OUTPUTDIR)" ] || rm -rf "$(OUTPUTDIR)"

.PHONY: regenerate
regenerate:
	"$(PELICAN)" -r "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

.PHONY: serve
serve:
	"$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

.PHONY: serve-global
serve-global:
	"$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -b $(SERVER)

.PHONY: devserver
devserver:
	"$(PELICAN)" -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

.PHONY: devserver-global
devserver-global:
	$(PELICAN) -lr $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -b 0.0.0.0

.PHONY: publish
publish:
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(PUBLISHCONF)" $(PELICANOPTS)

.PHONY: github
github: publish
	ghp-import --no-jekyll -m "Generate Pelican site" -b $(GITHUB_PAGES_BRANCH) "$(OUTPUTDIR)"
	git push origin $(GITHUB_PAGES_BRANCH)

.PHONY: install-git-hooks
install-git-hooks: .git/hooks/pre-commit

.git/hooks/%: git-hooks/%.sh
	install --mode=700 $< $@

.PHONY: install-ide-config
install-ide-config:
	rsync --recursive ide-config/ .

.PHONY: install-vale-styles
install-vale-styles:
	rm -rf styles/Google
	curl -sL https://github.com/errata-ai/Google/archive/v0.3.1.tar.gz \
	| tar zxf - -C styles/ --strip-components=1 Google-0.3.1/Google
	rm -rf styles/write-good
	curl -sL https://github.com/errata-ai/write-good/archive/v0.4.0.tar.gz \
	| tar zxf - -C styles/ --strip-components=1 write-good-0.4.0/write-good

.PHONY: lint
lint: lint-prose lint-python

.PHONY: lint-prose lint-python
lint-prose lint-python:
	./$@.sh

.PHONY: test-links-internal
test-links-internal: clean html
	linkchecker output/*.html

.PHONY: test-links-prod
test-links-prod:
	./test-links.sh
