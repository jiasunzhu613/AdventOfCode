import heapq
from collections import deque

file = open("../input.txt", "r")
grid = [i.strip() for i in file.readlines()]

# U D L R
dm = [(-1, 0), (1, 0), (0, -1), (0, 1)]
dir = {"^": dm[0], "v": dm[1], "<": dm[2], ">": dm[3]}

# part1 = -1
# visited = set()
# q = [(0, 0, grid[0].find("."), visited)]
# end = (len(grid) - 1, grid[-1].find("."))
#
# while q:
#     dist, r, c, vis = q.pop(-1)
#     if (r, c) == end:
#         part1 = max(dist, part1)
#     if (r, c) in vis:
#         continue
#     vis.add((r, c))
#     if grid[r][c] in dir:
#         dr, dc = dir[grid[r][c]]
#         rr = r + dr
#         cc = c + dc
#         if rr < 0 or rr >= len(grid) or cc < 0 or cc >= len(grid[0]):
#             continue
#         if grid[rr][cc] == "#":
#             continue
#         q.append((dist + 1, rr, cc, vis.copy()))
#     else:
#         for ele in dir:
#             dr, dc = dir[ele]
#             rr = r + dr
#             cc = c + dc
#             if rr < 0 or rr >= len(grid) or cc < 0 or cc >= len(grid[0]):
#                 continue
#             if grid[rr][cc] == "#":
#                 continue
#             q.append((dist + 1, rr, cc, vis.copy()))
#
# print(part1)


