from copy import copy
from itertools import combinations
import numpy as np
import os
from parse import parse, canonize
from simplex import calc_simplex_matrix, do_simplex
from matrix_multiplication import mult
import warnings

warnings.filterwarnings("ignore")

EPS = np.finfo(float).eps


def find_start_point(matrix):
    answers = matrix[:-1, -1]
    combs = combinations([i for i in range(0, matrix.shape[1] - 1)], matrix.shape[1] - matrix.shape[0])
    for i in combs:
        m = np.delete(matrix[:-1, :-1], list(i), 1)
        try:
            point = np.linalg.solve(m, answers)
        except np.linalg.LinAlgError:
            continue
        if all([x >= -EPS for x in point]):
            for j in i:
                point = np.insert(point, j, 0)
            return point
    print("Не получилось найти начальную точку")
    exit(0)


def main():
    # Считываем данные из нашего файла
    matrix, answers, target, conditions, start_point = parse('test/1.txt')
    flag = True
    if start_point == 'problem':
        start_point = None
        flag = False
    dimension = matrix.shape[1]
    matrix = canonize(matrix, answers, conditions)
    # Ищем начальную точку если она не задана
    if start_point is None:
        start_point = find_start_point(matrix)
    matrix, basis, not_basis = calc_simplex_matrix(matrix, start_point)
    x, f_ans = do_simplex(matrix, basis, not_basis)
    if flag:
        print(x[:dimension] / f_ans / target.value)
    else:
        print(f_ans * target.value, x[:dimension])
    a = x[:dimension] / f_ans / target.value
    if os.stat("test/2.txt").st_size == 0:
        exit(0)
    matrix, answers, target, conditions, start_point = parse('test/2.txt')
    matrix_new = copy(matrix[:-1])
    dimension = matrix.shape[1]
    matrix = canonize(matrix, answers, conditions)
    # Ищем начальную точку если она не задана
    if start_point is None:
        start_point = find_start_point(matrix)
    matrix, basis, not_basis = calc_simplex_matrix(matrix, start_point)
    x, f_ans = do_simplex(matrix, basis, not_basis)
    b = x[:dimension] / f_ans / target.value
    print(x[:dimension] / f_ans / target.value)
    print(mult(a, matrix_new, b))


if __name__ == '__main__':
    main()
