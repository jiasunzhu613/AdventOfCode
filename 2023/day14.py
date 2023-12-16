file = open("Inputs/day14.txt", "r")
grid = [list(i.strip()) for i in file.readlines()]

W = len(grid[0])
H = len(grid)
print(W, H)
part1 = 0
# Ideas:
for c in range(len(grid[0])):
    anchor = 0
    for r in range(len(grid)):
        if grid[r][c] == "#":
            anchor = r + 1
        elif grid[r][c] == "O":
            part1 += len(grid[0]) - anchor
            anchor += 1
print(part1)


# PART 2 IDEAS:
# - simulation/graph theory to find cycle length for each round rock?
# - east and west tilts do not affect load on north support beams (can this be used to optimize?)
def simulate(grid):
    temp = grid
    all_grids = []
    while True:
        def tiltNorth(grid):
            for c in range(len(grid[0])):
                anchor = 0
                for r in range(len(grid)):
                    if grid[r][c] == "#":
                        anchor = r + 1
                    elif grid[r][c] == "O":
                        grid[r][c] = "."
                        grid[anchor][c] = "O"
                        # rock_location[rock_location.index((r, c))] = (anchor, c)
                        anchor += 1
            return grid
        def tiltWest(grid):
            for r in range(len(grid)):
                anchor = 0
                for c in range(len(grid[0])):
                    if grid[r][c] == "#":
                        anchor = c + 1
                    elif grid[r][c] == "O":
                        grid[r][c] = "."
                        grid[r][anchor] = "O"
                        anchor += 1
            return grid
        def tiltSouth(grid):
            for c in range(len(grid[0]) - 1, -1, -1):
                anchor = len(grid) - 1
                for r in range(len(grid) - 1, -1, -1):
                    if grid[r][c] == "#":
                        anchor = r - 1
                    elif grid[r][c] == "O":
                        grid[r][c] = "."
                        grid[anchor][c] = "O"
                        anchor -= 1
            return grid
        def tiltEast(grid):
            for r in range(len(grid) - 1, -1, -1):
                anchor = len(grid) - 1
                for c in range(len(grid[0]) - 1, -1, -1):
                    if grid[r][c] == "#":
                        anchor = c - 1
                    elif grid[r][c] == "O":
                        grid[r][c] = "."
                        grid[r][anchor] = "O"
                        anchor -= 1
            return grid

        temp = tiltNorth(temp)
        temp = tiltWest(temp)
        temp = tiltSouth(temp)
        temp = tiltEast(temp)

        all_grids.append([row[:] for row in temp])
        for j in range(len(all_grids) - 1):
            if all_grids[j] == all_grids[-1]:
                return (j, all_grids[j: -1])
    return []

part2 = 0
stop, cycle = simulate(grid)
# for grid in cycle:
#     for j in grid:
#         print("".join(j))
#     print()
T = 10**9 - stop
MOD = T % len(cycle)
for r in range(H):
    for c in range(W):
        if cycle[MOD - 1][r][c] == "O":
            part2 += H - r

print(part2)
