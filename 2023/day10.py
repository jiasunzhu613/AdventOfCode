from collections import deque
file = open("../input.txt", "r")
grid = [i.strip() for i in file.readlines()]


"""
| is a vertical pipe connecting north and south. (0, 1), (0, -1)
- is a horizontal pipe connecting east and west. (1, 0), (-1, 0)
L is a 90-degree bend connecting north and east. (-1, -1), (1, 1)
J is a 90-degree bend connecting north and west. (-1, 1), (1, -1)
7 is a 90-degree bend connecting south and west. (-1, -1), (1, 1)
F is a 90-degree bend connecting south and east. (-1, 1), (1, -1)
"""

# PART 1
pipes = {}
symbols = "| - L J 7 F".split()
# format (col, row)
directions = [[(0, 1), (0, -1)], [(1, 0), (-1, 0)], [(0, -1), (1, 0)], [(0, -1), (-1, 0)]
              , [(0, 1), (-1, 0)], [(0, 1), (1, 0)]]

for i in range(len(symbols)):
    pipes[symbols[i]] = directions[i]

# locations the positions have to be if they want to use a certain pipe
# e.g. to use vertical pipe, you must be one row above it or one row below it
pipe_check = {}
# format (col, row)
directions_check = [[(0, -1), (0, 1)], [(-1, 0), (1, 0)], [(1, 0), (0, -1)], [(-1, 0), (0, -1)]
              , [(-1, 0), (0, 1)], [(1, 0), (0, 1)]]

for i in range(len(symbols)):
    pipe_check[symbols[i]] = directions_check[i]

dr = [0, 0, -1, 1]
dc = [-1, 1, 0, 0]
start = ()
for row in range(len(grid)):
    for col in range(len(grid[row])):
        if grid[row][col] == "S":
            start = (col, row)

def check(begin, pipe_position, pipe):
    for i in range(len(directions_check[0])):
        if begin[0] == pipe_position[0] + pipe_check[pipe][i][0] and begin[1] == pipe_position[1] + pipe_check[pipe][i][1]:
            return i
    return -1

visited = set()
distances = [[-1] * len(grid[0]) for i in range(len(grid))]
distances[start[1]][start[0]] = 0
dq = deque()
for i in range(len(dr)):
    rr = start[1] + dr[i]
    cc = start[0] + dc[i]
    if rr < 0 or rr >= len(grid) or cc < 0 or cc >= len(grid[0]):
        continue
    pipe = grid[rr][cc]
    if pipe == ".":
        continue

    index = check(start, (cc, rr), pipe)
    if index != -1:
        dq.append((1, cc, rr, index, pipe))

# just exit loop when reached start again
# main loop for bfs
while dq:
    dist, c, r, index_to_use, pipe = dq.popleft()
    distances[r][c] = dist
    cc = c + pipes[pipe][index_to_use][0]
    rr = r + pipes[pipe][index_to_use][1]
    if rr < 0 or rr >= len(grid) or cc < 0 or cc >= len(grid[0]):
        continue
    new_pipe = grid[rr][cc]
    if new_pipe == "S":
        break
    if distances[rr][cc] != -1:
        continue
    if new_pipe == ".":
        continue

    index = check((c, r), (cc, rr), new_pipe)
    if index != -1:
        dq.append((dist + 1, cc, rr, index, new_pipe))

part1 = -1
for i in distances:
    part1 = max(part1, max(i))
print(part1)


# PART 1
def getFarthest():
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if distances[r][c] == part1:
                return (r, c)
    return (-1, -1)

# GET FARTHEST NODE FROM START POINT
farthest = getFarthest()

# Find all nodes in main loop
main = set()
main.add(farthest)
queue = [farthest]
while queue:
    r, c = queue.pop(-1)
    if distances[r][c] == 0:
        continue
    for i in range(len(dr)):
        rr = r + dr[i]
        cc = c + dc[i]
        if rr < 0 or rr >= len(grid) or cc < 0 or cc >= len(grid[0]):
            continue
        if distances[rr][cc] == distances[r][c] - 1:
            queue.append((rr, cc))
            main.add((rr, cc))

# Expand the resolution of the grid so that nodes can squeeze
# through "0 width" corridors when we bfs later
expandedGrid = []
for r in range(len(grid)):
    row1 = []
    row2 = []
    row3 = []

    for c in range(len(grid[0])):
        if (r, c) in main:
            if grid[r][c] == "-":
                row1 += ["."] * 3
                row2 += ["x"] * 3
                row3 += ["."] * 3
            elif grid[r][c] == "|":
                row1 += [".", "x", "."]
                row2 += [".", "x", "."]
                row3 += [".", "x", "."]
            elif grid[r][c] == "7":
                row1 += [".", ".", "."]
                row2 += ["x", "x", "."]
                row3 += [".", "x", "."]
            elif grid[r][c] == "J":
                row1 += [".", "x", "."]
                row2 += ["x", "x", "."]
                row3 += [".", ".", "."]
            elif grid[r][c] == "F":
                row1 += [".", ".", "."]
                row2 += [".", "x", "x"]
                row3 += [".", "x", "."]
            elif grid[r][c] == "L":
                row1 += [".", "x", "."]
                row2 += [".", "x", "x"]
                row3 += [".", ".", "."]
            elif grid[r][c] == "S":
                row1 += [".", "x", "."]
                row2 += ["x", "x", "x"]
                row3 += [".", "x", "."]
        else:
            row1 += ["."] * 3
            row2 += ["."] * 3
            row3 += ["."] * 3
    expandedGrid.append(row1)
    expandedGrid.append(row2)
    expandedGrid.append(row3)

part2 = 0

# Precompute nodes that are guaranteed to be outside the loop so that we can ignore them later
# in bfs on expanded resolution grid
outside = [(0, 0), (0, len(grid[0]) - 1), (len(grid) - 1, 0), (len(grid) - 1, len(grid[0]) -1)]
processed = set()
for r, c in outside:
    queue = [(r, c)]
    while queue:
        r1, c1 = queue.pop(-1)
        if (r1, c1) in processed:
            continue
        processed.add((r1, c1))
        for i in range(len(dr)):
            rr, cc = r1 + dr[i], c1 + dc[i]
            if (rr, cc) in processed:
                continue
            if rr < 0 or rr >= len(grid) or cc < 0 or cc >= len(grid[0]):
                continue
            if (rr, cc) not in main:
                queue.append((rr, cc))

# Using expanded resolution grid to check if any nodes that arent directly part of the main loop
# can reach (0, 0)
# If a node can reach (0, 0), it means that it is outside of the main loop and shouldn't be
# counted toward the part2 counter
for r in range(len(grid)):
    for c in range(len(grid[0])):
        # ignore nodes we have already computed and know that are either
        # on the main loop or outside of the main loop
        if (r, c) in main or (r, c) in processed:
            continue

        # Check if some given node (r, c) can reach (0, 0)
        def canReachZeroZero(r, c):
            queue = [(r, c)]
            visited = set()
            while queue:
                r1, c1 = queue.pop(-1)
                visited.add((r1, c1))
                if (r1, c1) == (0, 0):
                    return True
                for i in range(len(dr)):
                    rr, cc = r1 + dr[i], c1 + dc[i]
                    if (rr, cc) in visited:
                        continue
                    if rr < 0 or rr >= len(expandedGrid) or cc < 0 or cc >= len(expandedGrid[0]):
                        continue
                    if expandedGrid[rr][cc] == ".":
                        queue.append((rr, cc))
            return False

        if not canReachZeroZero(r * 3, c * 3):
            part2 += 1

print(part2)