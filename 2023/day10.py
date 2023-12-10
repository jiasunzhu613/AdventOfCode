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
# print(start)
def check(begin, pipe_position, pipe):
    # print(pipe)
    for i in range(len(directions_check[0])):
        # print(begin[0], pipe_position[0] + pipe_check[pipe][i][0])
        # print(begin[1], pipe_position[1] + pipe_check[pipe][i][1])
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
    # print(index)
    if index != -1:
        dq.append((1, cc, rr, index, pipe))

# just exit loop when reached start again
# main loop for bfs
while dq:
    dist, c, r, index_to_use, pipe = dq.popleft()
    # print(pipe)
    # print(c, r)
    # print(dist, c, r, index_to_use, pipe)
    distances[r][c] = dist
    cc = c + pipes[pipe][index_to_use][0]
    rr = r + pipes[pipe][index_to_use][1]
    if rr < 0 or rr >= len(grid) or cc < 0 or cc >= len(grid[0]):
        continue
    new_pipe = grid[rr][cc]
    # print(cc, rr)
    # print(new_pipe)
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
farthest = ()
for i in distances:
    print(i)
    part1 = max(part1, max(i))
print(part1)
def getFarthest():
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if distances[r][c] == part1:
                return (r, c)
    return (-1, -1)

farthest = getFarthest()
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

def aboveNBelow(r, c):
    above = False
    temp = r
    temp += 1
    while 0 < temp < len(grid):
        if (temp, c) in main:
            above = True
            break
        temp += 1

    below = False
    temp = r
    temp -= 1
    while 0 < temp < len(grid):
        if (temp, c) in main:
            below = True
            break
        temp -= 1
    # print(above, below)
    return above and below

print(aboveNBelow(4, 7))
print(aboveNBelow(4, 8))
print(aboveNBelow(4, 9))

walls = set("L J 7 F |".split())
part2 = 0
for r in range(len(grid)):
    active = False
    for c in range(len(grid[0])):
        if (r, c) in main:
            if grid[r][c] in walls:
                # print(r, c, grid[r][c])
                active = not active
                continue
        # print((r, c), aboveNBelow(r, c))
        if active and aboveNBelow(r, c):
            print((r, c))
            part2 += 1
print(part2)