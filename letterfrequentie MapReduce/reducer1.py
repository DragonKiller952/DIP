import sys

# Input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.strip()
    # Replace all puntuation marks with $
    matrix = {i: {j: 0 for j in 'abcdefghijklmnopqrstuvwxyz $'} for i in 'abcdefghijklmnopqrstuvwxyz $'}

    # Use the bigram as keys, and add value to the value in matrix
    for item in eval(line):
        matrix[item[0][0]][item[0][1]] += item[1]

    # Create percentage for all following letters per beginning letter in matrix
    for i in 'abcdefghijklmnopqrstuvwxyz $':
        tot = sum(list(matrix[i].values()))
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if tot > 0 and matrix[i][j] > 0:
                matrix[i][j] = round((matrix[i][j] / tot) * 100, 1)

    print('%s\t' % (matrix))