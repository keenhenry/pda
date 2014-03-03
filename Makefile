# this script is build pda binary and install it 

PROJ_ROOT=/home/henry/Work/repos/pda

clean:
	rm $(PROJ_ROOT)/*.pyc $(PROJ_ROOT)/MANIFEST -rf

.PHONY: install
