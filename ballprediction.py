#mount google drive
from google.colab import drive
drive.mount('/content/drive')

#change directory 
cd drive/My Drive

"""# Import necessary module"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

#for encoding
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils

"""# Load the dataset"""

fileName ="Data- March-18-2019-SMOTE.csv"
df = pd.read_csv(fileName)     #read data from the link
df.shape

"""#drop unnecessary columns"""

dropCollumns = ['Match Date','Humidity/%','Age /years','Status','Speed/mph','Wicket','side','Innings','Mat','Inns','Balls','Runs','Wkts','Ave',	'Econ',	'SR',	'4w',	'5w',	'10']
df =df.drop(dropCollumns, axis=1)
df.shape

"""#drop unfilled rows"""

df = df.replace('?', np.nan).dropna()
df.shape

"""#some preprocessing"""

#convert to lower case
df =df.apply(lambda x: x.astype(str).str.lower())
df.head()

df["Ball Type"].value_counts()

#remove all first and last whitespace
df['Soil Type'] = df['Soil Type'].str.strip()
df['Match Location'] = df['Match Location'].str.strip()
df['Temperature/F'] = df['Temperature/F'].str.strip()
df['Dew Point/F'] = df['Dew Point/F'].str.strip()
df['Wind Speed/mph'] = df['Wind Speed/mph'].str.strip()
df['Ball Type'] = df['Ball Type'].str.strip()
df['Over'] = df['Over'].str.strip()
df['Direction'] = df['Direction'].str.strip()
df['Class'] = df['Class'].str.strip()

df['Ball Type'].value_counts()

df['Class'].value_counts()

"""# shuffle all data, encode the "Class" column & save it on a local variable"""

#shuffle all data
df = df.sample(frac=1).reset_index(drop=True)   # or df.sample(frac=1)

ytrain = np.asarray(df['Class'])

encoder = LabelEncoder()
encoder.fit(ytrain)
ytrain = encoder.transform(ytrain)

# convert integers to dummy variables (i.e. one hot encoded)
#ytrain= np_utils.to_categorical(encoded_Y)

df =df.drop(['Class'], axis=1)
df.shape

"""# Find out the categorical features"""

#find out the categorical column
# Categorical boolean mask
categorical_feature_mask = df.dtypes==object
# filter categorical columns using mask and turn it into a list
categorical_cols = df.columns[categorical_feature_mask].tolist()
categorical_cols

"""# label encode the categorical features"""

# instantiate labelencoder object
le = LabelEncoder()
# apply le on categorical feature columns
df[categorical_cols] = df[categorical_cols].apply(lambda col: le.fit_transform(col))

df.head()

"""# one hot encode the categorical features"""

# import OneHotEncoder
from sklearn.preprocessing import OneHotEncoder
# instantiate OneHotEncoder
ohe = OneHotEncoder(categorical_features = categorical_feature_mask, sparse=False ) 
# categorical_features = boolean mask for categorical columns
# sparse = False output an array not sparse matrix

# apply OneHotEncoder on categorical feature columns
df_ohe = ohe.fit_transform(df[0:]) # It returns an numpy array
df_ohe.shape

"""# split the dataset into train and test set"""

#split the dataset into feature and target
xtrain = df_ohe[:,:]
ytrain = ytrain

#split the dataset into train and test set
X_train, X_test, y_train, y_test = train_test_split(xtrain, ytrain, test_size=0.2,random_state=42)
print (X_train.shape, y_train.shape)
print (X_test.shape, y_test.shape)

"""#apply Gaussian Process Classifier and find the accuracy"""

from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF

kernel = 1.0 * RBF(1.0)
gpc = GaussianProcessClassifier(kernel=kernel,random_state=0).fit(X_train, y_train)
gpc.score(X_train, y_train)

gpc.score(X_test, y_test)

gpc.predict_proba(X_test[0:10])
#['dot->0', 'extra->1', 'high_run->2', 'low_run->3']

gpc.predict(X_test[0:500])

"""#apply Random Forest Classifier and find the accuracy"""

#Randomforest
from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)
clf.fit(X_train, y_train)  

clf.predict_proba(X_test)[0:10]

clf.score(X_train, y_train, sample_weight=None)

clf.score(X_test, y_test, sample_weight=None)

clf.predict(X_test[0:500])

"""#apply SVM and find the accuracy"""

#svm

from sklearn import svm
svm_clf = svm.SVC(gamma='scale', decision_function_shape='ovo')
svm_clf.fit(X_train, y_train)

svm_clf.score(X_train, y_train, sample_weight=None)

svm_clf.score(X_test, y_test, sample_weight=None)

svm_clf.predict(X_test[0:500])

"""#apply Gaussian Naive Bayes and find the accuracy"""

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)

gnb.score(X_train, y_train, sample_weight=None)

gnb.score(X_test, y_test, sample_weight=None)

gnb.predict(X_test[0:500])

"""#apply a deep nural network (LSTM) and find the accuracy"""

import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Dropout,LSTM

from tensorflow.python.keras.optimizers import Adam
from keras.models import Sequential

X_train.shape

X_train_new = X_train.reshape(X_train.shape[0],1,X_train.shape[1])
X_test_new = X_test.reshape(X_test.shape[0],1,X_test.shape[1])
X_test_new.shape

# convert integers to dummy variables (i.e. one hot encoded)
y_train_new = np_utils.to_categorical(y_train)
y_train_new = y_train_new.reshape(y_train_new.shape[0],1,y_train_new.shape[1])
print(y_train_new.shape)


y_test_new = np_utils.to_categorical(y_test)
y_test_new = y_test_new.reshape(y_test_new.shape[0],1,y_test_new.shape[1])
y_test_new.shape

# from tf.keras.models import Sequential  # This does not work!
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,Dropout, LSTM
from tensorflow.python.keras.optimizers import Adam

# Commented out IPython magic to ensure Python compatibility.
def myModel2():
  model = Sequential()
  model.add(LSTM(128,input_shape=(1,X_train_new.shape[2]), return_sequences=True))
  model.add(LSTM(64,return_sequences=True))
  model.add(LSTM(16,return_sequences=True))
  model.add(LSTM(8,return_sequences=True))
  model.add(Dense(4,activation='softmax'))
  optimizer = Adam(lr=.001)
  model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['accuracy', 'mae','mse'])
  model.summary()
  return model

def plot_accuracy_loss(history):
  history_dict = history.history
  # plot loss during training
  loss_values = history_dict['loss']
  val_loss_values = history_dict['val_loss']
  plt.subplot(211)
  plt.title('Loss')
  epochs = range(1, len(loss_values) + 1)
  plt.plot(epochs,loss_values, label='Training loss')
  plt.plot(epochs,val_loss_values, label='test/Validation loss')
  plt.xlabel('Epochs')
  plt.ylabel('Loss')
  plt.legend()
  # plot accuracy during training
  acc_values = history_dict['acc']
  val_acc_values = history_dict['val_acc']
  plt.subplot(212)
  plt.title('Accuracy')
  epochs = range(1, len(acc_values) + 1)
  plt.plot(epochs,acc_values, label='train accuracy')
  plt.plot(epochs,val_acc_values, label='test/Validation accuracy')
  plt.legend()
  plt.show()
  
def acc_on_train(x,y,model):
#   %%time
  result = model.evaluate(x, y,verbose=0)
  print("Accuracy on trian data: {0:.2%}".format(result[1]))
  print("MAE on train data: {0:.2%}".format(result[2]))
  print("MSE on train data: {0:.2%}".format(result[3]))
  print("\n")
  
def acc_on_test(x,y,model):
#   %%time
  result = model.evaluate(x, y,verbose=0)
  print("Accuracy on test data: {0:.2%}".format(result[1]))
  print("MAE on test data: {0:.2%}".format(result[2]))
  print("MSE on test data: {0:.2%}".format(result[3]))
  print("\n")

model = myModel2()

history = model.fit(X_train_new, y_train_new, epochs=20,validation_data=(X_test_new, y_test_new), batch_size=16)

# evaluate the model
acc_on_train(X_train_new,y_train_new,model)
acc_on_test(X_test_new,y_test_new,model)
plot_accuracy_loss(history)
