FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install curl -y
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install nodejs -y
RUN mkdir code
ADD . /code
WORKDIR "/code"
RUN ls
EXPOSE 4000
RUN apt-get install python-pip python-dev build-essential -y
RUN pip install keras
RUN pip install tensorflow
RUN pip install elasticsearch
RUN pip install pillow
RUN pip install h5py
RUN python pythonScript/load_vgg16.py
CMD ["npm", "run", "dev"]
