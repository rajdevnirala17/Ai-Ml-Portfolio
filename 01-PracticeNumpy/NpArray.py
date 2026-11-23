import numpy as np
arr = [1,2,3,4,5,6]
np_arr = np.array(arr)
print(np_arr)

np1= np_arr.reshape(2,3)#converting into 2d array
print(np1)
#array slicing
print(np_arr[0:6:2])
print(np1[0]) #first row
print(np1[:,2]) #(allrows,last column)
print(np1[0,1])#(first row,2nd column)
print(np1[:,-1])#(all rows,last column)
print(np1[1,1:])#(row1,from 1 column index to last element)

#NumPy operations
sum1 = np1.sum()
mean1 = np1.mean()
max1 = np1.max()
print(sum1)
print(mean1)
print(max1)

#adding and multiplying 2 with every element of an array
s1 = np_arr+2
m2 = np1*2
print(s1)
print(m2)
