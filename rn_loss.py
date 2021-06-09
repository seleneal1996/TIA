# -*- coding: utf-8 -*-
"""RN - Loss.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17psNu1NXGbaKfxU0d2v4wMgzfJczGK9R

# Log-Cosh Loss : 
logaritmo del coseno hiperbólico del error de predicción
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x_ds = [i for i in range(20)]
y_ds = [ i + np.random.normal(0,1) for i in x_ds ]

"""$h(x_i) = w_0 + w_1x_i$"""

def h(x,w):
  return w[0] + w[1]*x

"""$Error =  \sum_{i=0}^n \log (\cosh(y_i^p - y_i))$

$Error =  \sum_{i=0}^n \log (\cosh(h(x_i) - y_i))$
"""

def ErrorL(y,x,w):
 return sum( [ np.log(np.cosh(h(e[1],w) - e[0])) for  e in zip(y,x) ])

"""Calcular las derivadas 

$\frac{ \partial Error}{\partial w_0}  = \frac{1}{\cosh(h(x_i) - y_i)} \frac{ \partial }{\partial w_0} (\cosh (h(x_i) - y_i)) $

$ \frac{ \partial }{\partial w_0} (\cosh (h(x_i) - y_i)) = \sinh((h(x_i) - y_i))  \frac{ \partial }{\partial w_0}  (h(x_i) - y_i)$

$ \frac{ \partial Error}{\partial w_0}  =  \frac{\sinh((h(x_i) - y_i))  \frac{ \partial }{\partial w_0}  (h(x_i) - y_i)}{\cosh(h(x_i) - y_i))} = \frac{\sinh((h(x_i) - y_i))  }{\cosh(h(x_i) - y_i))} * \frac{ \partial }{\partial w_0}  (h(x_i) - y_i) $

$\frac{ \partial Error}{\partial w_0}  =  \tanh (h(x_i) - y_i)) * \frac{ \partial }{\partial w_0}  (h(x_i) - y_i) $

$\frac{ \partial Error}{\partial w_0}  =  \tanh (h(x_i) - y_i)) * 1 $

$\frac{ \partial Error}{\partial w_1}  =  \tanh (h(x_i) - y_i)) * x $
"""

def LogCosh(y,x,w):
  grad_w0 = sum([ np.tanh(h(e[1],w) - e[0])*(1)    for e in zip(y,x) ])
  grad_w1 = sum([ np.tanh(h(e[1],w) - e[0])*(e[1]) for e in zip(y,x) ])
  return grad_w0, grad_w1

#para comparar
matriz_error = []

w = np.random.rand(2) 

def trainL(x_ds, y_ds, w, epochs, alpha):
  list_error = []
  time = []
  for i in range(epochs):
    Err = ErrorL(y_ds,x_ds,w)
    list_error.append(Err)
    time.append(i)
    grad_w0, grad_w1 = LogCosh(y_ds,x_ds,w)
    w[0] = w[0] - alpha*grad_w0
    w[1] = w[1] - alpha*grad_w1

  matriz_error.append(time)
  matriz_error.append(list_error)
  return time,list_error

T,l = trainL(x_ds,y_ds, w, 10,0.0007)

plt.plot(T, l,'*')

plt.plot(x_ds, y_ds,'*')
plt.plot(x_ds, [ h(i,w) for i in x_ds])

