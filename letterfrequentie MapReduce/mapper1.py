import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.strip()
    line = ''.join([letter if letter in 'abcdefghijklmnopqrstuvwxyz ' else '$' for letter in line.lower()])
    line = [(line[i:i + 2], 1) for i in range(0, len(line) - 1)]

    print('%s\t' % (line))
