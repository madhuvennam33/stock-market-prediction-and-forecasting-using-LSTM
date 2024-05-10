# -*- coding: utf-8 -*-
"""stock market prediction

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HeGplteF3jOXf0K4rFv3Jm_d8PKDnFk8
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

df =pd.read_csv('https://raw.githubusercontent.com/mwitiderrick/stockprice/master/NSE-TATAGLOBAL.csv')
df=df.iloc[::-1]
df.head()

df.tail()

df.shape

df.columns

df.info()

df.describe()

#Data Preprocessing
df.isnull().sum()

duplicates= df.duplicated()
duplicates.value_counts()

df_high=df.reset_index()['High']
plt.plot(df_high)

"""As LSTM are not robust to the scale of the data, so we apply MinMax Scaler to transform our values in the range of 0 and 1.


"""

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0,1))
df_high = scaler.fit_transform(np.array(df_high).reshape(-1,1))

df_high.shape

df_high

#Split the data into train and test split
training_size = int(len(df_high) * 0.75)
test_size = len(df_high) - training_size
train_data,test_data = df_high[0:training_size,:], df_high[training_size:len(df_high),:1]

training_size, test_size

# convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

time_step = 100
x_train, y_train = create_dataset(train_data, time_step)
x_test, y_test = create_dataset(test_data, time_step)

#Reshape the input to be [samples, time steps, features] which is the requirement of LSTM
x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

print(x_train.shape), print(y_train.shape)

print(x_test.shape), print(y_test.shape)

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))
df_high=scaler.fit_transform(np.array(df_high).reshape(-1,1))

training_size=int(len(df_high)*0.65)
test_size=len(df_high)-training_size
train_data,test_data=df_high[0:training_size,:],df_high[training_size:len(df_high),:1]

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

### Create the Stacked LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences = True, input_shape = (100,1)))
model.add(LSTM(50, return_sequences = True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss = 'mean_squared_error', optimizer = 'adam')

model.summary()

model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs = 30, batch_size = 64, verbose = 1)

#predictions
#Lets predict and check performance metrics
train_predict = model.predict(x_train)
test_predict = model.predict(x_test)

#Transform back to original form
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

#Calculate RMSE performance metrics
import math
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(y_train, train_predict))

#Test Data RMSE
math.sqrt(mean_squared_error(y_test, test_predict))

#Plotting
#Shift train prediction for plotting
look_back = 100
trainPredictPlot = np.empty_like(df_high)
trainPredictPlot[:,:] = np.nan
trainPredictPlot[look_back:len(train_predict) + look_back, :] = train_predict

#Shift test prediction for plotting
testPredictPlot = np.empty_like(df_high)
testPredictPlot[:,:] = np.nan
testPredictPlot[len(train_predict) + (look_back * 2)+1:len(df_high) - 1, :] = test_predict

#Plot baseline and predictions
plt.plot(scaler.inverse_transform(df_high))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()

print("Green indicates the Predicted Data")
print("Blue indicates the Complete Data")
print("Orange indicates the Train Data")

#Predict the next 28 days Stock Price
len(test_data), x_test.shape

x_input = test_data[409:].reshape(1,-1)
x_input.shape

day_new = np.arange(1,101)
day_pred = np.arange(101,129)

day_new.shape

day_pred.shape

len(df_high)

data_new = df_high.tolist()
data_new.extend(lst_output)
plt.plot(data_new[2000:])

data_new =scaler.inverse_transform(data_new).tolist()

plt.plot(data_new)