FROM ubuntu:20.04
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -yq --no-install-recommends \
	sudo																		\
	git 																		\
	python3 																	\
	curl 																		\
	bash 																		\
	minizinc																	\
	python3-pip																	\
	&& curl -FsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - 		\
	&& apt install -yq nodejs npm 												\
	&& git clone https://www.github.com/krarty/battleships /         			\
	&& pip3 install -r /battleships/requirements.txt							\
	&& cd /battleships															\
	&& npm install																\
	&& rm -rf /var/lib/apt/lists/*


WORKDIR '/battleships'
CMD [ "/bin/sh", "-c", "npm run start" ]
