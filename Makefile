dev:
	python setup.py develop

dev-uninstall:
	python setup.py develop --uninstall
	rm `which pda` -rf
	rm pda.egg-info/ -rf

test:
	nosetests test_pda.py

clean:
	rm *.py[cod] MANIFEST -rf
