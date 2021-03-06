#!/usr/bin/make -f

SQLITE_DB=../workbench.db

all: install test

#.PHONY: install
install:
	pip $(SQLITE_DB)

#.PHONY: pip
#pip:
	# TODO: we need to install requirements.txt so XBlock is installed
	# from a GitHub repo.  Once XBlock is available through PyPi,
	# we can install all requirements using setup.py
#	pip install -r requirements.txt
#	pip install -e .
#	pip install -r test-requirements.txt

#$(SQLITE_DB):
	# The --noinput flag is for non-interactive runs, e.g. TravisCI.
#	python manage.py syncdb --noinput


testpy:
	python manage.py test -s --with-coverage --cover-xml
coverpy:
	/srv/sonar-runner/bin/sonar-runner -Dsonar.projectKey=multichoice -Dsonar.projectName=Multichoice -Dsonar.projectVersion=1.0 -Dsonar.sources="./multichoice" -Dsonar.sourceEncoding=UTF-8 -Dsonar.language=py -Dsonar.python.coverage.reportPath=coverage.xml

testjs:
	./tests/node_modules/.bin/karma start tests/karma.conf.js
coverjs:
	/srv/sonar-runner/bin/sonar-runner -Dsonar.projectKey=multichoice-js -Dsonar.projectName="Multichoice JS" -Dsonar.projectVersion="1.0" -Dsonar.sources="./multichoice/static/js/src" -Dsonar.sourceEncoding=UTF-8 -Dsonar.language=js -Dsonar.javascript.lcov.reportPath="tests/reports/report-lcov/lcov.info" -Dsonar.javascript.jstest.reportsPath="tests/reports/junit"