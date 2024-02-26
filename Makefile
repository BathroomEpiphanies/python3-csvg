$(shell touch -d @$(shell find src/deb -printf "%Ts\n" | sort -n | tail -n1) src/deb)
$(shell touch -d @$(shell find src/pypi -printf "%Ts\n" | sort -n | tail -n1) src/pypi)


VERSION := $(shell git tag --points-at HEAD | grep -vP '[^0-9.-]')
ifeq ($(VERSION),)
	VERSION := 0.0.0
endif
UNCOMMITED := $(shell git status -s)
ifneq ($(UNCOMMITED),)
	VERSION := 0.0.0
endif


DEBBUILDDIR := build/deb/python3-csvg_$(VERSION)_all
PYPIBUILDDIR := build/pypi


.PHONY: clean distclean deb pypi all

all: deb pypi
deb: build/deb/python3-csvg_$(VERSION)_all.deb
pypi: build/pypi/dist


build/deb/python3-csvg_$(VERSION)_all.deb: src/deb
	mkdir -p $(DEBBUILDDIR)
	rsync -a --copy-links --delete --delete-excluded --exclude '*~' --exclude '__pycache__' src/deb/ $(DEBBUILDDIR)/
	sed -e 's/VERSION/$(VERSION)/g' -i $(DEBBUILDDIR)/DEBIAN/control
	dpkg-deb --build --root-owner-group $(DEBBUILDDIR)


build/pypi/dist: src/pypi
	mkdir -p $(PYPIBUILDDIR)
	rsync -a --copy-links --delete --delete-excluded --exclude '*~' --exclude '__pycache__' src/pypi/ $(PYPIBUILDDIR)/
	sed -e 's/VERSION/$(VERSION)/g' -i $(PYPIBUILDDIR)/pyproject.toml
	python3 -m build $(PYPIBUILDDIR)


clean:
	rm -rf build
distclean:
	rm -rf build tmp
