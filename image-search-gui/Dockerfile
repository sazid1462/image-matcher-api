FROM ubuntu:16.04
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8
RUN apt-get update
RUN apt-get install curl -y
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN echo -ne '\n' | return
RUN apt-get install nodejs -y
RUN apt-get install git -y
RUN mkdir web
ADD . /web
WORKDIR "/web"
EXPOSE 8000
RUN npm run prestart
RUN npm run postinstall
CMD ["npm", "start"]
