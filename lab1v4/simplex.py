from math import inf

import numpy as np
from gauss import gauss_straight_run, gauss_reverse_run


def find_basis(matrix, point):
    k = matrix.shape[1] - matrix.shape[0]
    cnt = 0
    basis = []
    not_basis = []
    for i in range(len(point)):
        if point[i] == 0 and cnt < k:
            not_basis.append(i)
            cnt += 1
        else:
            basis.append(i)
    return basis, not_basis


def find_new_f(func, basis, not_basis, matrix_not_basis, answers):
    f_basis = np.delete(func, not_basis, 0)
    f_not_basis = np.delete(func, basis, 0)
    f_ans = 0
    for i in range(len(f_basis)):
        f_not_basis += f_basis[i] * matrix_not_basis[i]
        f_ans += f_basis[i] * answers[i]
    return f_not_basis, f_ans


def calc_simplex_matrix(matrix, start_point):
    basis, not_basis = find_basis(matrix, start_point)
    matrix_basis = np.delete(matrix[:-1, :-1], not_basis, 1)
    matrix_not_basis = np.delete(matrix[:-1, :-1], basis, 1)
    matrix_basis, matrix_not_basis, answers = gauss_straight_run(matrix_basis, matrix_not_basis, matrix[:-1, -1])
    matrix_not_basis, answers = gauss_reverse_run(matrix_basis, matrix_not_basis, matrix[:-1, -1], answers)
    f_not_basis, f_ans = find_new_f(matrix[-1, :-1], basis, not_basis, matrix_not_basis, answers)
    simplex_matrix = np.zeros((len(basis) + 1, len(not_basis) + 1))
    for i in range(len(basis)):
        simplex_matrix[i, -1] = answers[i]
        simplex_matrix[i, :-1] = matrix_not_basis[i]
    simplex_matrix[-1, -1] = f_ans
    simplex_matrix[-1][:-1] = f_not_basis
    return simplex_matrix, basis, not_basis


def find_r_column(matrix):
    ans = inf
    ans_column = -1
    for i in range(matrix.shape[1] - 1):
        if matrix[-1, i] < ans:
            ans = matrix[-1, i]
            ans_column = i
    return ans_column


def find_r_row(matrix, r_column):
    mn = +inf
    mn_ans = -1
    for i in range(matrix.shape[0] - 1):
        x = abs(matrix[i][-1] / matrix[i][r_column])
        if matrix[i][r_column] < 0 and x < mn:
            mn = x
            mn_ans = i
    if mn_ans == -1:
        print('Решения нет')
        exit(0)
    else:
        return mn_ans


def check(matrix):
    return min(matrix[-1][:-1]) < 0


def do_simplex(matrix, basis, not_basis):
    while check(matrix):
        r_column = find_r_column(matrix)
        r_row = find_r_row(matrix, r_column)
        m = matrix.copy()

        x = matrix[r_row][r_column]
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if i != r_row and j != r_column:
                    m[i][j] = matrix[r_row][r_column] * matrix[i][j] - matrix[i][r_column] * matrix[r_row][j]
        m[r_row] *= -1
        m[r_row][r_column] = 1
        matrix = m / x
        basis[r_row], not_basis[r_column] = not_basis[r_column], basis[r_row]
    v = np.zeros(matrix.shape[0] - 1 + matrix.shape[1] - 1)
    for i, ind in enumerate(basis):
        v[ind] = matrix[i, -1]
    return v, matrix[-1, -1]