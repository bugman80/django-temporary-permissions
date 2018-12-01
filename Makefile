VERSION=1.0.0
BUILDDIR=~build
PIP_VERSION=18.1
PIP_DOWNLOAD_CACHE=
PIP_QUIETLY?=
DBENGINE?=postgres
DJANGO_2?='django>=2.1,<2.2'
DJANGO_DEV=git+https://github.com/django/django.git


info:
	# [info]
	# current dir: ${PWD}
	# virtualenv dir: ${VIRTUAL_ENV}
	@python -c "import sys; print('# python: {}'.format(sys.version.replace('\n', '')))"
	@echo "#" `pip -V`
	@python -c "import setuptools; print('# setuptools: {}'.format(setuptools.__version__))"
	# DBENGINE: ${DBENGINE}
	# DJANGO: ${DJANGO}


init:
	python manage.py syncdb --noinput
	pip install -r django_temporary_permissions/requirements/install.pip


test:
	py.test


clean:
	# [clean]
	@rm -rf ${BUILDDIR} dist *.egg-info .coverage .pytest MEDIA_ROOT MANIFEST .cache *.egg build STATIC
	@find . -name .cache -prune | xargs rm -rf
	@find . -name __pycache__ -prune | xargs rm -rf
	@find . -name "*.py?" -prune | xargs rm -rf
	@find . -name "*.orig" -prune | xargs rm -rf
	@rm -f coverage.xml flake.out pep8.out pytest.xml


develop:
	pip install -U pip setuptools
	@pip install -qr django_temporary_permissions/requirements/install.pip
	@pip install -qr django_temporary_permissions/requirements/testing.pip


build-dir:
	# [build-dir]
	@mkdir -p ${BUILDDIR}/coverage


fullclean: clean
	find . -name *.sqlite -prune | xargs rm -rf
	rm -fr .tox


coverage:
	py.test --junitxml=pytest.xml --create-db --cov=django_temporary_permissions --cov-report=html --cov-config=tests/.coveragerc
	# firefox ${BUILDDIR}/coverage/index.html


pep8:
	pep8 django_temporary_permissions


clonedigger:
	mkdir -p ${BUILDDIR}
	clonedigger django_temporary_permissions -l python -o ${BUILDDIR}/clonedigger.html --ignore-dir=migrations,tests --fast


docs:
	mkdir -p ${BUILDDIR}/
	sphinx-build -aE docs/ ${BUILDDIR}/docs
	# firefox ${BUILDDIR}/docs/index.html


.PHONY: docs


install-django:
	@sh -c "if [ '${DJANGO}' = '2.1.x' ]; then pip install ${PIP_QUIETLY} ${DJANGO_2}; fi"
	@sh -c "if [ '${DJANGO}' = 'dev'   ]; then pip install ${PIP_QUIETLY} ${DJANGO_DEV}; fi"
	@echo "# installed  Django=="`django-admin.py --version`


init-db:
	@sh -c "if [ '${DBENGINE}' = 'postgres' ]; then psql -c 'DROP DATABASE IF EXISTS dj_temp_perm;' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'postgres' ]; then psql -c 'CREATE DATABASE dj_temp_perm;' -U postgres; fi"


ci_test: info clean build-dir develop init-db
	@pip install -q pip==${PIP_VERSION}
	@${MAKE} install-django

	@${MAKE} coverage
	@flake8 django_temporary_permissions | tee ${BUILDDIR}/flake.out
	@pep8 django_temporary_permissions | tee ${BUILDDIR}/pep8.out
