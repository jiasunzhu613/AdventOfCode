file = open("Inputs/day16.txt", "r")
grid = [i.strip() for i in file.readlines()]

H = len(grid)
W = len(grid[0])
relative_position = {(0, 1): "l",
                     (0, -1): "r",
                     (1, 0): "t",
                     (-1, 0): "b"}
def line(dr, dc):
    if relative_position[(dr, dc)] in "tb":
        return [(dr, dc)]
    return [(1, 0), (-1, 0)]

def dash(dr, dc):
    if relative_position[(dr, dc)] in "lr":
        return [(dr, dc)]
    return [(0, 1), (0, -1)]

def forward_slant(dr, dc):
    # return negative reciporcal
    return [(-dc, -dr)]

def backward_slant(dr, dc):
    # return negative reciporcal
    return [(dc, dr)]

def solve(start, dir):
    # MAIN TAKEAWAY: Recognizing that we can track visited based on the direction each node comes from
    # - We dont need to follow a new node that has been visited by a previous node with the same directional matrices
    # as it will lead down to the same path
    # - If we store direction matrices in our visited array, we can keep track of which directions has visited each node
    # and which unique paths have not been processed
    seen = [[[] for i in range(W)] for j in range(H)]
    queue = []
    queue.append((start[0], start[1], dir[0], dir[1]))
    energy = [[False] * W for _ in range(H)]
    while queue:
        r, c, dr, dc = queue.pop(-1)
        if r < 0 or r >= H or c < 0 or c >= W:
            continue
        if (dr, dc) in seen[r][c]:
            continue

        energy[r][c] = True # add to some grid?
        seen[r][c].append((dr, dc))
        if grid[r][c] == ".":
            queue.append((r + dr, c + dc, dr, dc))
        elif grid[r][c] == "/":
            for ddr, ddc in forward_slant(dr, dc):
                queue.append((r + ddr, c + ddc, ddr, ddc))
        elif grid[r][c] == "\\":
            for ddr, ddc in backward_slant(dr, dc):
                queue.append((r + ddr, c + ddc, ddr, ddc))
        elif grid[r][c] == "|":
            for ddr, ddc in line(dr, dc):
                queue.append((r + ddr, c + ddc, ddr, ddc))
        elif grid[r][c] == "-":
            for ddr, ddc in dash(dr, dc):
                queue.append((r + ddr, c + ddc, ddr, ddc))
    return sum(sum(i) for i in energy)

# part 1
part1 = solve((0, 0), (0, 1))
print(part1)

best = []
best.append(solve((0, 0), (1, 0)))
best.append(solve((0, 0), (0, 1)))
for c in range(1, W - 1):
    best.append(solve((0, c), (1, 0)))

best.append(solve((0, W - 1), (1, 0)))
best.append(solve((0, W - 1), (0, -1)))
for r in range(1, H - 1):
    best.append(solve((r, W - 1), (0, -1)))

best.append(solve((H - 1, W - 1), (-1, 0)))
best.append(solve((H - 1, W - 1), (0, -1)))
for c in range(1, W - 1):
    best.append(solve((H - 1, c), (-1, 0)))

best.append(solve((H - 1, 0), (-1, 0)))
best.append(solve((H - 1, 0), (0, 1)))
for r in range(1, H - 1):
    best.append(solve((r, 0), (0, 1)))

part2 = max(best)
print(part2)

