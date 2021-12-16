FROM ubuntu:20.04
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -yq  \
	sudo									\
	nodejs 									\
	git 									\
	python3 								\
	curl 									\
	bash 									\
	&& curl -FsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - 	\
	&& git clone https://www.github.com/krarty/battleships 					\
	&& rm -rf /var/lib/apt/lists/*


CMD [ "/bin/sh", "-c", "cd battleships && yarn start" ]
