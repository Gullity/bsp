FIREFOX_LATEST_VERSION = $(shell curl https://github.com/mozilla/geckodriver/releases/latest | cut -d "/" -f 8 | cut -d "\"" -f 1)


ifeq ($(shell uname -s),Linux)
	DISTRO=linux64
    DISTRO_FIREFOX=linux64
else
	DISTRO=mac64
    DISTRO_FIREFOX=macos
endif

ifndef PYENV_HOME
	ifdef VIRTUAL_ENV
		PYENV_HOME=${VIRTUAL_ENV}
	else
		PYENV_HOME ?=.venv
	endif
endif

define download_the_firefox_browser
	wget https://github.com/mozilla/geckodriver/releases/download/${FIREFOX_LATEST_VERSION}/geckodriver-${FIREFOX_LATEST_VERSION}-${DISTRO_FIREFOX}.tar.gz \
	-P external/selenium/; \
	tar -xzf external/selenium/geckodriver-${FIREFOX_LATEST_VERSION}-${DISTRO_FIREFOX}.tar.gz --directory external/selenium/; \
	chmod +x external/selenium/geckodriver;
endef


help: ## help: Show this help message.
	@echo "usage: make [target] ..."
	@echo ""
	@echo "targets:"
	@grep -Eh '^.+:(\w+)?\ ##\ .+' ${MAKEFILE_LIST} | cut -d ' ' -f '3-' |  column -t -s ':' | egrep --color '^[^ ]*'

chromedriver: ## chromedriver: Download Chrome webdriver for selenium
	@make print MSG="\n\n\n======== Downloading Chromedriver ========\n\n\n"
	if [ ! -f external/selenium/chromedriver ]; then \
		mkdir -p external/selenium; \
		wget http://chromedriver.storage.googleapis.com/$(shell curl http://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_${DISTRO}.zip \
		-P external/selenium/; \
		unzip external/selenium/chromedriver_${DISTRO}.zip -d external/selenium/; \
		chmod +x external/selenium/chromedriver; \
	fi;

firefoxdriver: ## firefoxdriver: Download firefox webdriver for selenium
	@make print MSG="\n\n\n======== Downloading Firefoxdriver ========\n\n\n"
	if [ ! -f external/selenium/geckodriver ]; then \
		mkdir -p external/selenium; \
	    $(call download_the_firefox_browser) \
	fi;

print:
	@echo "\033[0;33m"
	@echo $$MSG
	@echo "\033[0m"

test:  ## Run tests.
	${PYENV_HOME}/bin/behave bsp
