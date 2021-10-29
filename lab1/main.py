import re
from copy import copy, deepcopy
from operator import itemgetter


def parse(str):
    str = str.replace(' ', '')
    str1 = re.split('<=|>=|=', str)
    b = str1[1]
    str1 = str1[0]
    count = int(str1[-1:]) + 1
    ans = []
    for i in range(1, count):
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
    if str[str.find(f'={b}') - 1] != '<' and str[str.find(f'={b}') - 1] != '>':
        sign = '='
    else:
        sign = str[str.find(f'={b}') - 1] + '='
    return ans, float(b), sign


def simplex(func, system, basis):
    bas_not_nan = [k for k, v in enumerate(basis) if v != 0]
    bas_nan = [k for k, v in enumerate(basis) if v == 0]
    arr = []
    count = 0
    #переводим нашу систему в матрицу
    for equation, bas in zip(system, bas_not_nan):
        arr.append([])
        ###
        arr[count].append((equation[1]) / equation[0][bas])
        for k, el in enumerate(basis):
            if k != bas:
                el = equation[0][k] * -1 / equation[0][bas]
                arr[count].append(el)
            else:
                arr[count].append(0)
        ###
        count += 1
    arr1 = deepcopy(arr)
    for array, bas in zip(arr1, bas_not_nan):
        for i in range(len(array)):
            array[i] *= func[bas]
    arr.append([])
    for column in range(len(arr1[0])):
        summ = 0
        for row in range(len(arr1)):
            summ += arr1[row][column]
        arr[count].append(summ)
    for i in bas_nan:
        arr[count][i + 1] += func[i]
    index = min(enumerate(arr[-1][1:]), key=itemgetter(1))[0]
    basis = [[v, k + 1] for k, v in enumerate(basis)]
    while arr[-1][index + 1] <= 0:
        mas = []
        for i in range(len(arr) - 1):
            if arr[i][index + 1] < 0:
                mas.append((arr[i][0] / arr[i][index + 1], i))
        if not mas:
            print(arr)
            return 'Нет решения'
        row = min(mas, key=lambda t: abs(t[0]))[1]
        column = index + 1
        for i in range(len(arr)):
            if i != row:
                for j in range(len(arr[i])):
                    if j != column:
                        arr[i][j] = arr[i][j] * arr[row][column] - arr[i][column] * arr[row][j]
        for i in range(len(arr[row])):
            if i != column:
                arr[row][i] *= -1
        arr = [list(map(lambda x: x/arr[row][column], z)) for z in arr]
        count1 = 0
        count2 = 0
        swap1 = swap2 = 0

        for i in range(len(basis)):
            if basis[i][0] == 0:
                count2 += 1
            else:
                count1 += 1
            if count1 == row + 1:
                swap1 = i
            if count2 == column:
                swap2 = i
        basis[swap1][1], basis[swap2][1] = basis[swap2][1], basis[swap1][1]
        index = min(enumerate(arr[-1][1:]), key=itemgetter(1))[0]
    count = 0
    for i in basis:
        if i[0] != 0:
            i[0] *= arr[count][0]
            count += 1
    basis.sort(key=lambda x: x[1])
    return ", ".join(f"x{k+1} = " + str(v[0]) for k, v in enumerate(basis)) + f", min = {arr[-1][0]}"


print(simplex([-1, -2, -3, 1], [parse('x1 - 3x2 - x3 - 2x4 = -4'), parse('x1 - x2 + x3 + 0x4 = 0')], basis=[2, 2, 0, 0]))
