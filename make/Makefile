# this script is build pda binary and install it 

PROJ_ROOT=/home/henry/Work/repos/pda
SOURCE_DIR=${PROJ_ROOT}/src
INSTALL_DIR=${PROJ_ROOT}/bin

all:
	@echo "Please run 'make install'"

install:
	@echo ""
	mkdir -p $(INSTALL_DIR)
	chmod u+x $(SOURCE_DIR)/pda.py
	cp -p $(SOURCE_DIR)/pda.py $(INSTALL_DIR)/pda
	@echo "Installation completed. The binary is installed in '$(INSTALL_DIR)'"
	@echo ''

clean:
	rm $(INSTALL_DIR) -rf

.PHONY: install
