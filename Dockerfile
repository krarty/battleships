FROM ubuntu:20.04
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -yq  \
	sudo									\
	git 									\
	python3 								\
	curl 									\
	bash 									\
	&& curl -FsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - 		\
	&& apt install -yq nodejs npm 												\
	&& rm -rf /var/lib/apt/lists/*


CMD [ "/bin/sh", "-c", "git clone https://www.github.com/krarty/battleships && cd battleships && npm install && npm run start" ]
