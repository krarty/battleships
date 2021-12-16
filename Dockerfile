FROM ubuntu:20.04
RUN apt update && apt install -y 			\
	build-essential 						\
	nodejs 									\
	git 									\
	python3 								\
	curl 									\
	bash 									\
	&& curl -FsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - 	\
	&& git clone https://www.github.com/krarty/battleships 					\
	&& rm -rf /var/lib/apt/lists/*
	
CMD cd battleships && yarn serve & && python3 solver/server/solver.py
