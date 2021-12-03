from matplotlib import pyplot as plt
from math import sqrt, inf
from copy import deepcopy
from random import random

import numpy as np


def generator(num):
    a = np.array([random() for i in range(num)])
    a /= a.sum()
    return a


a = generator(8)
b = np.array([generator(8) for j in range(8)]).reshape(8, 8)

sko = []


def compare(a, b):
    diff = 0
    for i in zip(a, b):
        diff += (i[0] - i[1]) ** 2
    diff = sqrt(diff / len(a))
    sko.append(diff)
    return diff


def ergodich(a, b, e):
    prev = deepcopy(a)
    prev[0] = -inf
    while compare(a, prev) > e:
        prev = a
        a = a.dot(b)
    return a


print(ergodich(a, b, 0.0001))
print(sko)
step =[]
for i in range(len(sko)):
    step.append(i + 1)
plt.figure(figsize=(10, 8))
plt.plot(step, sko)
plt.title('СКО', fontsize=15)
plt.xlabel('шаг', fontsize=14)
plt.ylabel('ско', fontsize=14)
plt.show()
