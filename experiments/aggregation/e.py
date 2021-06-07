from scipy.stats import norm
import numpy as np


mu, sigma = 0.4, 0.15 # mean and standard deviation
s = np.random.normal(mu, sigma, 10)


import time

# creating a time delay of 5 seconds


# creating and Initilizing a list
myList = ['Jai', 'Shree', 'RAM', "5", 'August', "2020"]

# the list will be displayed after the delay of 5 seconds
for i in myList:
    print(i)
    time.sleep(5)