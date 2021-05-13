import sys

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    matrix = {i: {j: 0 for j in 'abcdefghijklmnopqrstuvwxyz $'} for i in 'abcdefghijklmnopqrstuvwxyz $'}
    for item in eval(line):
        matrix[item[0][0]][item[0][1]] += item[1]
    for i in 'abcdefghijklmnopqrstuvwxyz $':
        tot = sum(list(matrix[i].values()))
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if tot > 0 and matrix[i][j] > 0:
                matrix[i][j] = round((matrix[i][j] / tot) * 100, 1)

    print('%s\t' % (matrix))