from keras.applications.vgg16 import VGG16

def main():
    VGG16(weights='imagenet', include_top=False, pooling = 'max')
    pass

if __name__ == "__main__":
    main()
