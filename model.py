#!/usr/bin/env python
# coding: utf-8

# In[3]:


from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers, callbacks
import warnings
import pickle
warnings.filterwarnings("ignore")


# re-size all the images to this
IMAGE_SIZE = [224, 224]

train_path = '/Trash Data/Train'
valid_path = '/Trash Data/Test'

# add preprocessing layer to the front of VGG
vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# don't train existing weights
for layer in vgg.layers:
    layer.trainable = False
  

  
  # useful for getting number of classes
folders = glob('Trash Data/Train/*')
  

# our layers - you can add more if you want
x = Flatten()(vgg.output)
# x = Dense(1000, activation='relu')(x)
prediction = Dense(len(folders), activation='softmax')(x)

# create a model object
model = Model(inputs=vgg.input, outputs=prediction)

# view the structure of the model
model.summary()

# tell the model what cost and optimization method to use
model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)


from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('Trash Data/Train/',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('Trash Data/Test/',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')

"""early_stopping = callbacks.EarlyStopping(
    min_delta=0.001, # minimium amount of change to count as an improvement
    patience=0, # how many epochs to wait before stopping
    restore_best_weights=True,
)"""

# fit the model
r = model.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=10,
  #callbacks=[early_stopping],
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

"""import tensorflow as tf

from keras.models import load_model"""

"""model.save('facefeatures_new_model.h5')"""


# In[13]:

""""
from keras.preprocessing.image import load_img
import numpy as np
from keras.preprocessing import image
from numpy import expand_dims
from matplotlib import pyplot

from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from numpy import expand_dims
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from keras.utils.vis_utils import plot_model
from keras.preprocessing.image import img_to_array

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16

image1 = load_img('image.jpg', target_size=(224, 224))
image1 = img_to_array(image1)
# reshape data for the model
print(image1.shape)
image1 = image1.reshape((1, image1.shape[0], image1.shape[1], image1.shape[2]))
print(image1.shape)

# prepare the image for the VGG model
image1 = preprocess_input(image1)

yhat = model.predict(image1, verbose=0)[0]
print(yhat)
print(yhat.max())

   


# In[7]:


training_set.class_indices"""


# In[ ]:
"""pickle.dump(model,open('model.pkl','wb'))
model1=pickle.load(open('model.pkl','rb'))"""


"""
joblib.dump(model,open('model.pkl','wb'))
model1 = joblib.load(open('model.pkl','rb'))"""

"""import joblib
joblib.dump(model,open('model.pkl','wb'))
model1 = joblib.load(open('model.pkl','rb'))"""
model1=model.save('model.h5')