#!/usr/bin/env python
# coding: utf-8



import warnings
warnings.filterwarnings("ignore")



from pathlib import Path
import pathlib
import os.path
import os
os.environ['PYTHONHASHSEED'] = '0'



from PIL import Image
import PIL


from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import *
from keras import models, layers, optimizers                  
from tensorflow.keras.models import load_model



from keras.applications.inception_v3 import InceptionV3





### Loading data 
train = Path("")

train_dir = Path('./forest_fire_data/Training_and_Validation')
train_filepaths = list(train_dir.glob('*/*.jpg'))

test_dir = Path('./forest_fire_data/Testing')
test_filepaths = list(test_dir.glob('*/*.jpg'))




image_count_train = len(list(train_dir.glob('*/*.jpg')))
print(image_count_train)

image_count_test = len(list(test_dir.glob('*/*.jpg')))
print(image_count_test)



# ### Create a dataset


train =  ImageDataGenerator(rescale = 1/255)

test = ImageDataGenerator(rescale = 1/255)

rn.seed(42)
train_dataset = train.flow_from_directory("./forest_fire_data/Training_and_Validation/",
                                          target_size=(150,150),
                                          batch_size = 32,
                                          class_mode = 'binary')
                                         
test_dataset = test.flow_from_directory("./forest_fire_data/Testing/",
                                          target_size=(150,150),
                                          batch_size =32,
                                          class_mode = 'binary',
                                          shuffle=False)












# ### Model Training

# InceptionV3 

# In[11]:


# Build the Model
def build_model(base_conv) :
    
    rn.seed(42)
    model = models.Sequential()
    model.add(base_conv)
    model.add(layers.Flatten())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    base_conv.trainable = False

  
    
    return model
    


base_inc = InceptionV3 (weights='imagenet', 
                     include_top=False,
                 input_shape=(150, 150, 3))

model_inc = build_model(base_inc)





model_inc.compile(loss='binary_crossentropy', 
             optimizer='Adam', 
             metrics=['acc'],
             run_eagerly=True)
   


history_inc = model_inc.fit(train_dataset, epochs=10,
                    validation_data=test_dataset)










def evaluation(model):
    test_loss, test_acc = model.evaluate(test_dataset)
    print('test acc:', test_acc)
    print('test_loss:',test_loss)
    Y_pred = model.predict(test_dataset)
   
    
evaluation(model_inc) 



# ### Saving the choosing model 

model_inc.save('model_inc_final.h5', save_format='h5')


# ### Convert model to TFLite

import tensorflow as tf
import keras
model = keras.models.load_model('model_inc_final.h5')

converter = tf.lite.TFLiteConverter.from_keras_model(model)

model_lite = converter.convert()



with open('model.tflite', 'wb') as f_out:
    f_out.write(model_lite)

