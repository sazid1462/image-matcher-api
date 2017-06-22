if [ ! -d data ]; then
  mkdir $data
fi
docker-compose build
