# Requirements
  * OS: ubuntu 16.04(Recomended), or any linux based os, or unix based docker machine
  * docker (>=17.05.0-ce)
  * docker-compose (>=1.11.2)

# How to build
  * run `chmod +x fileName` on `build.sh` and `up.sh` file.
  * run `build.sh`
  * run `up.sh`
  * access localhost:8000 in browser

# Tech Stack
  * keras (Machine learning library built on theano and tensorflow)
  * nodejs
  * angularjs
  * docker
  * elasticsearch

# Description Similarity Algorithm
  * ## Steps of the Algorithm
    - Load image
    - Extract features from the image for all previously uploaded images
    - Calculate cosine similarity with the current image
    - Update best 3 images
    - Save current image features for next iteration

  * ## Loading Image
    - We used keras library to load images from a physical location. And then converted it to an array of integers. After reducing the dimension for efficient calculation we preprocess the image array and use it to predict features.

  * ## Extract Features from Image
    - For predicting features of an image we used VGG16 pre-trained library from Keras. It is a flexible accurate image feature extractor. It gives the flexibility to remove the top layer of predictors and returns a feature array length of 512.
  * ## Cosine Similarity
    - For each previously saved images, we calculate the cosine similarity of features of that image and the current image. And on the process, we filter out top 3 most relevant images.