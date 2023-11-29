import csv
import matplotlib.pyplot as plt


import matplotlib.pyplot as plt

# Data lists
x = []
sqr = []
mul = []
div = []

with open('100k_slots.txt') as f:
    i =1
    for line in f:
        cols = line.split(',')
        #print(cols)
        x.append(i)
        i+=1
        sqr.append(int(cols[0]))
        mul.append(int(cols[1]))
        div.append(int(cols[2]))

# Plot
# print(x)
# print(sqr)
# print(mul)
# print(div)
fig, ax = plt.subplots()
ax.scatter(x, sqr, label='Square',c='g')
ax.scatter(x, mul, label='Mul',c='r')
ax.scatter(x, div, label='Div', c='b')
# ax.set_xbound(lower=0, upper=1000)
ax.set_ylim(0, 1000)
ax.hlines(200, xmin=min(x), xmax=max(x), colors='r', linestyles='--')
ax.legend()
plt.show()
