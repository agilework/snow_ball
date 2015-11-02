__author__ = 'admin'
#-*- coding: utf-8 -*-
import numpy as np

arr_1 = np.array(['a','b'])
np.save("test",arr_1)

arr_2 = np.load("test.npy")
print arr_2
print np.random.randn(4,4)