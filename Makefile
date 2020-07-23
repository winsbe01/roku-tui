configure:
	if [ ! -d ~/.config/roku ]; \
	then mkdir ~/.config/roku; \
	fi
	cp roku.config ~/.config/roku

install:
	cp roku-cli.py /usr/local/bin/roku
