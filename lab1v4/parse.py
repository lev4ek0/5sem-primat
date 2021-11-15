import re
from enum import Enum

import numpy as np


class Target(Enum):
    MIN = 1
    MAX = -1


class Condition(Enum):
    GT = -1
    LT = 1
    EQ = 0


def find_columns(arr):
    max = 0
    for i in range(1, len(arr) - 1):
        k = arr[i].split('=')[0].split('x')[-1].split(' ')[0]
        if int(k) > max:
            max = int(k)
    return max


def find_func(str1, columns_len):
    if '->' in str1:
        str1 = str1.split('->')[0].replace(' ', '')
    elif '=' in str1:
        str1 = str1.split('=')[0].replace(' ', '')
        if str1[-1] == '>' or str1[-1] == '<':
            str1 = str1[:-1]
    ans = []
    for i in range(1, columns_len + 1):
        if f'x{i}' not in str1:
            ans.append(0)
            continue
        coeff = re.split('-|\\+', str1.split(f'x{i}')[0])[-1:][0]
        if not coeff:
            a = str1.find(f'x{i}')
            if not a:
                ans.append(1)
            else:
                ans.append(float(f'{str1[a - 1]}1'))
        else:
            a = str1.find(f'{coeff}x{i}')
            if not a:
                ans.append(float(coeff))
            else:
                ans.append(float(str1[a - 1] + coeff))
    return ans


def find_x(str):
    str = str[1:-1]
    return list(map(float, str.replace(' ','').split(',')))


def parse(filename):
    with open(filename) as f:
        arr = []
        for line in f:
            arr.append(line)
        conditions_len = len(arr) - 2
        columns_len = find_columns(arr)
        target = Target.MIN if arr[0].split('->')[1].replace(' ', '').split('\n')[0] == 'min' else Target.MAX
        matrix = np.zeros((conditions_len + 1, columns_len))
        answers = np.array([0 for _ in range(conditions_len + 1)])
        func = find_func(arr[0], columns_len)
        matrix[conditions_len] = np.array(func)
        conditions = [Condition.EQ for _ in range(conditions_len)]
        # invert coefficient to change on minimization
        if target == Target.MAX:
            matrix[conditions_len] *= -1
        for i in range(1, conditions_len + 1):
            if arr[i].split('=')[0][-1] in ['<=', '<']:
                cond_type = Condition.LT
            elif arr[i].split('=')[0][-1] in ['>=', '>']:
                cond_type = Condition.GT
            else:
                cond_type = Condition.EQ
            cond_ans = float(arr[i].split('=')[1])
            coef = find_func(arr[i], columns_len)
            matrix[i - 1] = np.array(coef)
            answers[i - 1] = cond_ans
            conditions[i - 1] = cond_type
        start_point_str = arr[-1]
        if start_point_str in ['x0 = None', 'x0 =']:
            start_point = None
        else:
            start_point = np.array(find_x(start_point_str.split('=')[1].replace(' ', '')))
        return matrix, answers, target, conditions, start_point


def canonize(matrix: np.array, answers: np.array, conditions):
    not_eq = len(list(filter(lambda x: x != Condition.EQ, conditions)))
    m = np.zeros((matrix.shape[0], matrix.shape[1] + not_eq + 1))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            m[i, j] = matrix[i, j]
        m[i, m.shape[1] - 1] = answers[i]
    for i, c in enumerate(conditions):
        if c != Condition.EQ:
            if c == Condition.GT:
                m[i, matrix.shape[1] + i] = -1
            else:
                m[i, matrix.shape[1] + i] = +1
    return m