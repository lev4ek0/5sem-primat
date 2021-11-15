from math import inf

import numpy as np


def max_row(row: np.array, column_num: int, start_row: int):
    mx = -inf
    mx_ans = -1
    for i in range(start_row, row.shape[0]):
        if abs(row[i][column_num]) > mx:
            mx = abs(row[i][column_num])
            mx_ans = i
    return mx_ans


def gauss_straight_run(matrix_basis: np.array, matrix_not_basis: np.array, answers: np.array):
    for i in range(matrix_basis.shape[0] - 1):
        row = max_row(matrix_basis, i, i)
        if i != row:
            matrix_basis[[i, row]] = matrix_basis[[row, i]]
            matrix_not_basis[[i, row]] = matrix_not_basis[[row, i]]
            answers[[i, row]] = answers[[row, i]]
        for j in range(i + 1, matrix_basis.shape[0]):
            if matrix_basis[i][i] == 0:
                raise ZeroDivisionError("Детерминант равен нулю")
            c = matrix_basis[j][i] / matrix_basis[i][i]
            matrix_basis[j] = [
                matrix_basis[j][k] - matrix_basis[i][k] * c
                for k in range(matrix_basis.shape[0])
            ]
            matrix_not_basis[j] = [
                matrix_not_basis[j][k] - matrix_not_basis[i][k] * c
                for k in range(matrix_not_basis.shape[1])
            ]
            answers[j] -= answers[i] * c
    return matrix_basis, matrix_not_basis, answers


def gauss_reverse_run(matrix_basis: np.array, matrix_not_basis: np.array, start_answers: np.array, answers: np.array):
    matrix_not_basis = -matrix_not_basis
    for i in range(matrix_basis.shape[0] - 1, -1, -1):
        c = matrix_basis[i][i]
        matrix_not_basis[i] = [matrix_not_basis[i][j] / c for j in range(matrix_not_basis.shape[1])]
        answers[i] /= c
        matrix_basis[i] = [matrix_basis[i][j] / c for j in range(matrix_basis.shape[0])]
        for j in range(i + 1, matrix_basis.shape[0]):
            matrix_not_basis[i] -= matrix_basis[i][j] * matrix_not_basis[j]
            start_answers[i] -= start_answers[j] * matrix_basis[i][j]
    return matrix_not_basis, answers