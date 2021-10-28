import re
from copy import copy
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
    arr = []
    arr1 = []
    count = 0
    for equation, bas in zip(system, bas_not_nan):
        arr.append([])
        our_bas = copy(bas_not_nan)
        our_bas.remove(bas)
        sum = 0
        for i in our_bas:
            sum += equation[0][i]
        arr[count].append((equation[1] - sum) / equation[0][bas])
        for k, el in enumerate(basis):
            if not el:
                el = equation[0][k] * -1 / equation[0][bas]
                arr[count].append(el)
        arr1.append([x * func[bas_not_nan[count]] for x in arr[count]])
        count += 1
    sum = 0
    xes = [0] * (len(arr1[0]) - 1)
    for k, v in enumerate(arr1):
        sum += v[0]
        for key, value in enumerate(arr1[k][1:]):
            xes[key] += value
    bas_nan = [k for k, v in enumerate(basis) if v == 0]
    for k, i in enumerate(bas_nan):
        xes[k] += func[i]
    arr.append([sum]+xes)
    print(arr)
    index = min(enumerate(arr[-1][1:]), key=itemgetter(1))[0]
    if arr[-1][index + 1] >= 0:
        return 'Дальше нельзя оптимизировать'
    else:
        mas = []
        for i in range(len(arr)):
            if arr[i][index + 1] < 0:
                mas.append((arr[i][0] / arr[i][index + 1], i))
        if not mas:
            return 'Бесконечное число решений'
        print(min(mas))


simplex([-1, -2, -2, -1], [parse('x1 - x3 + 0.5x4 = 1'), parse('x2 + x3 - x4 = 1')], basis=[1, 1, 0, 0])

