from collections import deque

file = open("../input.txt", "r")
grid = [i.strip() for i in file.readlines()]
H = len(grid)
W = len(grid[0])

dist = [[-1] * W for _ in range(H)]

start = ()
for r in range(H):
    for c in range(W):
        if grid[r][c] == "S":
            start = (r, c)

dr = [0, 0, -1, 1]
dc = [-1, 1, 0, 0]
queue = deque()
queue.append((0, start[0], start[1]))
MAX = 64
while queue:
    steps, r, c = queue.popleft()
    if dist[r][c] != -1:
        continue
    dist[r][c] = steps
    for i in range(len(dr)):
        rr, cc = r + dr[i], c + dc[i]
        if rr < 0 or rr >= H or cc < 0 or cc >= W:
            continue
        if grid[rr][cc] == "#":
            continue
        queue.append((steps + 1, rr, cc))

part1 = 0
for r in range(H):
    for c in range(W):
        if dist[r][c] == -1:
            continue

        if dist[r][c] % 2 == 0 and MAX % 2 == 0 and dist[r][c] <= MAX:
            part1 += 1

for i in dist:
    print(i)
print(part1)