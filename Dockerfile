FROM ubuntu:20.04
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -yq  \
	sudo									\
	git 									\
	python3 								\
	curl 									\
	bash 									\
	&& curl -FsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - 		\
	&& curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - 	\
	&& echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list \
	&& apt install -yq nodejs yarn 												\
	&& git clone https://www.github.com/krarty/battleships 						\
	&& rm -rf /var/lib/apt/lists/*


CMD [ "/bin/sh", "-c", "cd battleships && yarn start" ]
