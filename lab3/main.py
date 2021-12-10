import sys

from matplotlib import pyplot as plt
from math import sqrt, inf
from copy import deepcopy
from random import random, seed
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def generator(num):
    a = np.array([random() for i in range(num)])
    a /= a.sum()
    return a


a = np.zeros(8)
a[0] = 1
seed(10)
b = np.array([generator(8) for j in range(8)]).reshape(8, 8)


def compare(a, b, sko):
    c = a - b
    diff = np.std(c)
    sko.append(diff)
    return diff


def number(a, b, e, step, sko):
    prev = deepcopy(a)
    prev[0] = -sys.float_info.max
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


plt.style.use('ggplot')
sko = []
print(number(a, b, 0.0001, 10, sko))
print(anal(b), '\n')
step = []
for i in range(len(sko)):
    step.append(i)
grid = plt.GridSpec(2, 3, wspace=0.5, hspace=0.5)
plt.subplot(grid[0, 2])
plt.plot(step, sko, 'magenta')
step1 = deepcopy(step)
sko1 = deepcopy(sko)
plt.xlabel('шаг', fontsize=14)
plt.xticks(step)
plt.ylabel('ско', fontsize=14)
seed(1111)
b = np.array([generator(8) for j in range(8)]).reshape(8, 8)
step.clear()
sko.clear()
print(number(a, b, 0.0001, 10, sko))
print(anal(b))
for i in range(len(sko)):
    step.append(i)
plt.subplot(grid[1, 2])
plt.plot(step, sko, 'lime')
plt.xlabel('шаг', fontsize=14)
plt.xticks(step)
plt.ylabel('ско', fontsize=14)
plt.subplot(grid[:2, :2])
plt.plot(step1, sko1, 'magenta')
plt.xlabel('шаг', fontsize=14)
plt.ylabel('ско', fontsize=14)
plt.plot(step, sko, 'lime')
plt.xlabel('шаг', fontsize=14)
plt.ylabel('ско', fontsize=14)
plt.show()
