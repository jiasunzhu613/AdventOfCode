import math
file = open("../input.txt", "r")
commands = [i.strip() for i in file.readlines()]

def find_determinant(x1, x2, y1, y2):
    return (x1*y2) - (y1*x2)

# have -1 intially for first node that wont be counted through code
# areas are -1 because we are doing shoelace theorem in the clockwise direction!
part1 = -1
part2 = -1

mapped = {"0": (1, 0), "1": (0, -1), "2": (-1, 0), "3": (0, 1), "L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}
start1 = [0, 0]
start2 = [0, 0]

for command in commands:
    a, b, c = command.split()
    dir1 = mapped[a]
    amount1 = int(b)

    c = c[2:-1]
    dir2 = mapped[c[-1]]
    amount2 = int(c[:-1], 16)

    # get coords
    x1, y1 = start1
    x2, y2 = x1 + dir1[0], y1 + dir1[1]
    # find determinant
    det = find_determinant(x1, x2, y1, y2)
    # add to counter
    part1 += det * amount1
    part1 += -1 * amount1
    # set new coordinate
    start1 = [x1 + dir1[0] * amount1, y1 + dir1[1] * amount1]

    # get coords
    x1, y1 = start2
    x2, y2 = x1 + dir2[0], y1 + dir2[1]
    # find determinant
    det = find_determinant(x1, x2, y1, y2)
    # add to counter
    part2 += det * amount2
    part2 += -1 * amount2
    # set new coordinate
    start2 = [x1 + dir2[0] * amount2, y1 + dir2[1] * amount2]

print(math.ceil(abs(part1/2)))
print(math.ceil(abs(part2/2)))




