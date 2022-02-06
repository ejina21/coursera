import sys

for i in range(int(sys.argv[1])):
    print(" " * (int(sys.argv[1]) - i - 1) + "#" * (i + 1))