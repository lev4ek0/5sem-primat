from matplotlib import pyplot as plt
from math import sqrt, inf
from copy import deepcopy
from random import random

import numpy as np


def generator(num):
    a = np.array([random() for i in range(num)])
    a /= a.sum()
    return a


a = np.zeros(8)
a[0] = 1
b = np.array([generator(8) for j in range(8)]).reshape(8, 8)


def compare(a, b, sko):
    diff = 0
    for i in zip(a, b):
        diff += (i[0] - i[1]) ** 2
    diff = sqrt(diff / len(a))
    sko.append(diff)
    return diff


def number(a, b, e, step, sko):
    prev = deepcopy(a)
    prev[0] = -inf
    i = 0
    while compare(a, prev, sko) > e and i < step:
        i += 1
        prev = a
        a = a.dot(b)
    return a


def anal(b):
    e = np.eye(8)
    b = b.T
    b = b - e
    b[7] = np.ones(8)
    answers = np.zeros(8)
    answers[7] = 1
    return np.linalg.solve(b, answers)


sko = []
print(number(a, b, 0.0001, 10, sko))
print(anal(b), '\n')
step = []
for i in range(len(sko)):
    step.append(i)
plt.figure(figsize=(5, 4))
plt.plot(step, sko, 'magenta')
plt.title('СКО', fontsize=15)
plt.xlabel('шаг', fontsize=14)
plt.ylabel('ско', fontsize=14)
b = np.array([generator(8) for j in range(8)]).reshape(8, 8)
step.clear()
sko.clear()
print(number(a, b, 0.0001, 10, sko))
print(anal(b))
for i in range(len(sko)):
    step.append(i)
plt.plot(step, sko, 'lime')
plt.show()
