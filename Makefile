.PHONY: devinstall devuninstall test clean lint

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*

lint:
	! pylint -rn pda/ 	# make `make` ignore error return code

devinstall:
	python setup.py develop

devuninstall:
	python setup.py develop --uninstall
	rm `which pda` -rf
	rm pda.egg-info/ -rf

test:
	tox

clean: devuninstall
	rm MANIFEST -rf
	rm .tox* -rf
	rm *egg/ -rf
	rm *egg-info/ -rf
	rm dist/ -rf
	find . -iname .tox -prune -o -iname '*.py[cod]' -print | xargs rm -rf
