import math
file = open("../input.txt", "r")
commands = [i.strip() for i in file.readlines()]

# Legacy part1 was solve for complement and then subtract from total area
def legacyPart1():
    W = 600
    H = 600
    grid = [["."] * W for _ in range(H)]

    dm = {"L": (0, -1),
          "R": (0, 1),
          "U": (-1, 0),
          "D": (1, 0)}
    r = H//2
    c = W//2
    grid[r][c] = "#"
    for command in commands:
        direction, amount, colour = command.split()
        for _ in range(int(amount)):
            r += dm[direction][0]
            c += dm[direction][1]
            grid[r][c] = "#"

    dr = [0, 0, -1, 1]
    dc = [-1, 1, 0, 0]
    def solve(start):
        queue = []
        queue.append(start)
        visited = set()
        while queue:
            r, c = queue.pop(-1)
            if grid[r][c] == "#":
                continue

            if (r, c) in visited:
                continue
            visited.add((r, c))
            for i in range(len(dr)):
                rr = r + dr[i]
                cc = c + dc[i]
                if rr < 0 or rr >= H or cc < 0 or cc >= W:
                    continue
                queue.append((rr, cc))
        return len(visited)

    outside = [[False] * W for _ in range(H)]
    queue = [(0, 0)]

    while queue:
        r, c = queue.pop(-1)
        if grid[r][c] == "#":
            continue
        if outside[r][c]:
            continue
        outside[r][c] = True
        for i in range(len(dr)):
            rr = r + dr[i]
            cc = c + dc[i]
            if rr < 0 or rr >= H or cc < 0 or cc >= W:
                continue
            queue.append((rr, cc))

    total_area = W*H
    return total_area - sum(sum(i) for i in outside)

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




