import sys

# Input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.strip()

    # Each letter in the line gets checked and replaced if the letter is invalid
    line = ''.join([letter if letter in 'abcdefghijklmnopqrstuvwxyz ' else '$' for letter in line.lower()])

    # The line gets turned into a bigram format so that the reducer can read it
    line = [(line[i:i + 2], 1) for i in range(0, len(line) - 1)]

    print('%s\t' % (line))
