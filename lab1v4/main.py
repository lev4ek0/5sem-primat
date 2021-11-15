from itertools import combinations
import numpy as np

from parse import parse, canonize
from simplex import calc_simplex_matrix, do_simplex

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
    matrix, answers, target, conditions, start_point = parse('lab1v3/1.txt')
    dimension = matrix.shape[1]
    matrix = canonize(matrix, answers, conditions)
    # Ищем начальную точку если она не задана
    if start_point is None:
        start_point = find_start_point(matrix)
    matrix, basis, not_basis = calc_simplex_matrix(matrix, start_point)
    x, f_ans = do_simplex(matrix, basis, not_basis)
    print(f_ans * target.value, x[:dimension])


if __name__ == '__main__':
    main()
