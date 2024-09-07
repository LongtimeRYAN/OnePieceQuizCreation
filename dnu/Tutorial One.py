import this


# Write your code here :-)
#load the numpy library and matplot lib
import numpy as np
import matplotlib.pyplot as plt

#read data file and skip the header
fname='oscilloscope_signal.csv'
np.genfromtxt(fname, ts)

#define a linerally spaced array with 100 points for x
x=np.linspace(-2, 2, 100)

y=x**2

#plot data
plt.plot(x,y)
plt.show()