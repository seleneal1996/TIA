# -*- coding: utf-8 -*-
"""RNN_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q4A9ALJ0n-8FjE2e2O3LCieZ58UshxY4
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.preprocessing import MinMaxScaler

x = torch.rand(1000,1,5)
print(x.shape)
lstm = nn.LSTM(5,2,1)
print(lstm.eval())
#p , _= lstm(x)
#print(p.shape)
print([p.shape for p in lstm.parameters()])
# wxh (4*hidde_size, input)
# whh (4*hidde_size, hizen_size)
# bxh (4*hidde_size)
# bhh (4*hidde_size)

input_size = 100
hidden_size = 500
num_layers = 1

#input [seq_len, batch, input_size]

#model = nn.LSTM(input_size, hidden_size, num_layers)

#train(model, optimizer, loss_function, num_epochs, trainX, trainY)

#print([p.shape for p in model.parameters()])

#print(model.weight_ih_l0.shape)

from google.colab import  drive
drive.mount('/content/drive')
path = '/content/drive/MyDrive/Colab Notebooks/dataset_RNN.csv'
training_set = pd.read_csv(path)
training_set = training_set.iloc[:,1:2].values
 #plt.plot(training_set)
#plt.show()
print(training_set)
sc = MinMaxScaler()
training_set = sc.fit_transform(training_set)
print(training_set)
print('****************************')

datos  = torch.tensor(training_set)
print(datos.shape)
datos = datos.squeeze(-1)
print(datos.shape)
datos = datos.type(torch.float) 
print(datos.shape)

def Window(data, lenght_windows):
  lenght_data = data.shape[0]
  data_x = torch.zeros(lenght_data - lenght_windows-1, lenght_windows)
  data_y =  torch.zeros(lenght_data - lenght_windows-1)
  # 
  for i in range(lenght_windows):
    data_x[:,i] = data[i:lenght_data - lenght_windows -1 + i] 
  # Se añade una dimensióón adicional a la salida [n,1]
  data_y = data[lenght_windows:].unsqueeze(-1)
  return data_x.unsqueeze(-1), data_y 

train_size = int(len(datos) * 0.8)
test_size = len(datos) - train_size

seq_length = 4
x, y = Window(datos, seq_length)

train_size = int(len(y) * 0.8)
test_size = len(y) - train_size

trainX, trainY  = x[:train_size],y[:train_size]
testX, testY = x[train_size:],y[train_size:]

class LSTM(nn.Module):

    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        #h_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size))
        #c_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size))
        ula, (h_out, _) = self.lstm(x)
        h_out = h_out.view(-1, self.hidden_size)
        out = self.fc(h_out)
        return out

def train(model, optmizer, loss_f, num_epochs, data_train_x, data_train_y):

  for epoch in range(num_epochs):
      
      outputs = model(data_train_x)
      loss = loss_f(outputs, data_train_y)
      
      optimizer.zero_grad()
      loss.backward()
      
      optimizer.step()
      if epoch % 100 == 0:
        print("Epoch: %d, loss: %1.5f" % (epoch, loss.item()))

# Hiperparametros
num_epochs = 1000
learning_rate = 0.01

input_size = 1
hidden_size = 2
num_layers = 1

model = LSTM(input_size, hidden_size, num_layers)
loss_function = torch.nn.MSELoss()    
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

train(model, optimizer, loss_function, num_epochs, trainX, trainY)

model.eval()
prediction = model(x)
data_predict = prediction.data.numpy()
dataY_plot = y.data.numpy()


plt.figure(figsize=(20,5))
#plt.xlim([2220,3000])
plt.axvline(x=train_size, c='r', linestyle='--')
plt.plot(dataY_plot)
plt.plot(data_predict)
plt.legend(["","Real","predicted"])
plt.suptitle('Time-Series Prediction')

plt.show()

trainX.shape

model.eval()

prediction = model(testX)
print(prediction.shape)
data_predict = prediction.data.numpy()

dataY_plot = testY.data.numpy()


plt.figure(figsize=(20,5))
#plt.xlim([2220,3000])
#plt.axvline(x=train_size, c='r', linestyle='--')
plt.plot(dataY_plot)
plt.plot(data_predict)
plt.legend(["","Real","predicted"])
plt.suptitle('Test Resul')

plt.show()

class GRU_model(nn.Module):

    def __init__(self, input_size, hidden_size, num_layers):
        super(GRU_model, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.GRU = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
          h_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size))
          #c_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size))
          h_out, _ = self.gru(x, h_0.detach())
          h_out = h_out[:, -1, :]
          #h_out = h_out.view(-1, self.hidden_size)
          h_out = self.fc(h_out)
          return h_out

def train(model, optmizer, loss_f, num_epochs, data_train_x, data_train_y):

  for epoch in range(num_epochs):
      
      outputs = model(data_train_x)
      loss = loss_f(outputs, data_train_y)
      
      optimizer.zero_grad()
      loss.backward()
      
      optimizer.step()
      if epoch % 100 == 0:
        print("Epoch: %d, loss: %1.5f" % (epoch, loss.item()))

# Hiperparametros
num_epochs = 1000
learning_rate = 0.01

input_size = 1
hidden_size = 2
num_layers = 1
model=nn.GRU(input_size, hidden_size, num_layers)
loss_function = torch.nn.MSELoss()    
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

train(model, optimizer, loss_function, num_epochs, trainX, trainY)

model.eval()
prediction = model(x)
data_predict = prediction.data.numpy()
dataY_plot = y.data.numpy()


plt.figure(figsize=(20,5))
#plt.xlim([2220,3000])
plt.axvline(x=train_size, c='r', linestyle='--')
plt.plot(dataY_plot)
plt.plot(data_predict)
plt.legend(["","Real","predicted"])
plt.suptitle('Time-Series Prediction')

plt.show()

trainX.shape

model.eval()

prediction = model(testX)
print(prediction.shape)
data_predict = prediction.data.numpy()

dataY_plot = testY.data.numpy()


plt.figure(figsize=(20,5))
#plt.xlim([2220,3000])
#plt.axvline(x=train_size, c='r', linestyle='--')
plt.plot(dataY_plot)
plt.plot(data_predict)
plt.legend(["","Real","predicted"])
plt.suptitle('Test Resul')

plt.show()













