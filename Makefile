
.PHONY: all

.PHONY: i18n-extract i18n-init i18n-update i18n-compile i18n-merge
.PHONY: weblate-merge

all: projectlogo.png

%.png: %.svg
	inkscape --export-dpi=75 --export-overwrite --export-type=png $<


# ---- i18n support ---—
# Run babel via setup.py so babel picks up the config from setup.cfg

WEBLATE=https://translate.codeberg.org/git/pdftools/pdfposter/
PACKAGE_DIR=pdfposter
DOMAIN=pdfposter
WEBLATE_BRANCH=develop

# For every update
i18n-extract:
	mkdir -p ${PACKAGE_DIR}/locale
	python setup.py extract_messages \
	  --input-dirs=${PACKAGE_DIR},$(shell \
              python -c "import argparse;print(argparse.__file__)")
	git commit -m "i18n: Update translation template file (.pot)." \
	  ${PACKAGE_DIR}/locale/${DOMAIN}.pot

# once per language
i18n-init:
	python setup.py init_catalog --locale "${language}"

i18n-update: i18n-extract
	python setup.py update_catalog
	echo "Now edit the messages and run 'make i18n-compile' for testing"

# Catalog are automatically compiled by setup.py when running sdist.
i18n-compile:
	python setup.py compile_catalog

i18n-merge: weblate-merge
weblate-merge:
	git remote -v | grep -cq weblate || \
		git remote add weblate ${WEBLATE}
	git fetch weblate ${WEBLATE_BRANCH}
	git merge --no-edit weblate/${WEBLATE_BRANCH}
