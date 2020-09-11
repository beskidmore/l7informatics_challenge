# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:47:35 2020

@author: Benjamin Skidmore
"""
##Here we test Benford's assertion 

##import libraries
import numpy as np
import matplotlib.pyplot as plt
import math
import statistics

# read items in the list and separate by all white space into strings.
def read_by_tokens(fileobj):
    for line in fileobj:
        for token in line.split():
            yield token
            
states = ['New','W','N', 'S']
#make list that will hold data while it is operated on            
A = []
## read census_2009b POINT THIS TO THE LOCATION OF census_2009b
with open('C:/Users/Ben/Desktop/Life/Resumes/Summer-2020/L7informatics/data/census_2009b') as f:
    # make refilling list for operations and future insertion into list comprehensions
    lst = []
    for token in read_by_tokens(f):
        # if a float we want a newline on the next item
        if '.' in token and 'St.' != token and 'Ste.' != token:
            lst.append(token)
            #if names are more than 1 word for city/state
            while len(lst) >6:
                #if state concat column 0 and 1
                if lst[0] in states:
                    lst[0] = lst[0] + ' ' +lst[1]
                    del lst[1]
                #if city concat until the length is less than 6. For long city names
                else:
                    lst[1] = lst[1] + ' ' +lst[2]
                    del lst[2]

            A.append(lst)
            lst = []
        ## Extend the list if not a float (all are strings but only the last numbers contain decimals)    
        else:
            lst.append(token)
#convert list comprehension into numpy array
B = np.array(A)        
#print the cleaned numpy array
print(B)

#remove header for analysis
B = np.delete(B, (0), axis=0)
        


##Part2 
# Be able to split number into its numeric components
def split(word): 
    return [char for char in word]
# list we will append first integers to for plotting with later
i_lst=[]
## parse the numpy array, read 3rd column, read number and find leading intiger, append to list.
for x in range(len(B)):
    numb = B[x][2]
    n = split(numb)
    i_lst.append(int(n[0]))
iarray = np.array(i_lst)
#print(iarray)

#Use numpy to make a histogram of the distribution of leading numbers
np.arange(1,10)
hist,edges = np.histogram(iarray,bins= np.arange(1,11))
print('Count of all leading digits in the census data starting from 1:',  hist)
##make sure it is counted correctly
count =0
for i in iarray:
    if i == 1:
        count +=1
#print(count)
        
#How often is '1' the leading digit?
print('1 is the leading digit this % of the time in census data:', hist[0]/sum(hist))
#29% of the time, this agrees with Benford's assertion




#Part 3
##plot histogram of leading number distribution
plt.bar(np.arange(1,10),hist)
plt.title("Benford's law testing census data", fontsize=14)
plt.xticks(np.arange(1,10), fontsize=13)
plt.yticks(fontsize=13)
plt.xlabel('Number', fontsize = 13)
plt.ylabel('Count', fontsize =13)
plt.show()

#expected distribution:
import random
randomlist =[]
for i in range(0,sum(hist)):
    randomlist.append(random.randint(1,9))
#now get the histogram of distributions
randarray = np.array(randomlist)
randhist,randedges = np.histogram(randarray,bins= np.arange(1,11))
print('Count of all leading digits in the random data starting from 1:',randhist)

## Benford's test of the random distribution
print('1 is the leading digit this % of the time in random data:' ,randhist[0]/sum(randhist))
#We get '1' as the first digit only ~10% of the time in the random distribution

#plot again but with random distribution
# set x axis groups and bar width
width = 0.35 #width of bars
ind = np.arange(9) #x locations of the groups

# plot 
fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2,hist, width, label = 'Census distribution')
rects2 = ax.bar(ind + width/2,randhist, width, label = 'Random distribution')
plt.title("Benford's law testing census data", fontsize=14)
plt.xticks(np.arange(1,10), fontsize=13)
plt.yticks(fontsize=13)
plt.xlabel('Number', fontsize = 13)
plt.ylabel('Count', fontsize =13)
ax.legend()
fig.tight_layout()
plt.show()    



#chi square to see if distribution is random:
from scipy.stats import chisquare
chisquare(hist, f_exp=randhist)
print('Chi-squared test for independence of number selection in census data',chisquare(hist, f_exp=randhist))
print('p-value is <0.5 so there is a statistical non-randomness to the census data')
# Power_divergenceResult(statistic=9342.003802447034, pvalue=0.0)
# The p-value is <0.05 so there is a statistical non-randomness to the census data.


## Runs Test to see if each distribution is random
def runsTest(l, l_median): 
    runs, n1, n2 = 0, 0, 0
    # Checking for start of new run 
    for i in range(len(l)): 
        # no. of runs 
        if (l[i] >= l_median and l[i-1] < l_median) or \
                (l[i] < l_median and l[i-1] >= l_median): 
            runs += 1  
        # no. of positive values 
        if(l[i]) >= l_median: 
            n1 += 1   
        # no. of negative values 
        else: 
            n2 += 1   
    runs_exp = ((2*n1*n2)/(n1+n2))+1
    stan_dev = math.sqrt((2*n1*n2*(2*n1*n2-n1-n2))/ \
                       (((n1+n2)**2)*(n1+n2-1))) 
    z = (runs-runs_exp)/stan_dev 
    return z 
# produce median of the data
lr_median= statistics.median(randomlist) 


# if Z > 1.96 than the data is not random to a 95% confidance interval.
#for the randomly generated data:
Zr = abs(runsTest(randomlist, lr_median))

print("Runs test for random distribution, if Z > 1.96 than the data is not random to a 95% confidance interval.") 
print('Random distribution Z-statistic= ', Zr)
# 0.679

# for the census data:
l_median= statistics.median(i_lst) 
Z = abs(runsTest(i_lst, l_median)) 
print('Census distribution Z-statistic= ', Z)
#1.86
