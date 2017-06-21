if [ ! -d data ]; then
  mkdir $data
fi
cd server
if [ ! -d uploads ]; then
  mkdir uploads
fi
cd ..
docker-compose build
