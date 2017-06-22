FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install curl -y
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN -y
RUN apt-get install nodejs -y
RUN mkdir web
ADD . /image-search-gui
WORKDIR "/web"
EXPOSE 8000
RUN npm install
CMD ["npm", "start"]
