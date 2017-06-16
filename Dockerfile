FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install curl -y
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install nodejs python -y
RUN mkdir code
ADD . /code
WORKDIR "/code"
RUN ls
RUN npm install
EXPOSE 4000
CMD ["npm", "run", "dev"]
