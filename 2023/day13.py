file = open("Inputs/day13.txt", "r")
input = [i.strip() for i in file.read().split("\n\n")]

grids = []
for line in input:
    grids.append(line.split("\n"))


P = 27
M = 10**9 + 7


def findReflection(rowHashes, colHashes, innequate, TYPE):
    # find a center
    T = "" # type of symmetry
    longest = -1
    ret = (-1, -1)

    # Row check for even center
    counter = -1
    center = (-1, -1)
    for i in range(len(rowHashes) - 1):
        count = 0
        l = i
        r = i + 1
        while l > -1 and r < len(rowHashes):
            if rowHashes[l] == rowHashes[r]:
                count += 1
            else:
                break
            l -= 1
            r += 1
        if count > counter and (l == -1 or r == len(rowHashes)):
            if TYPE == "R":
                if (i, i + 1) != innequate:
                    counter = max(counter, count)
                    center = (i, i + 1)
            else:
                counter = max(counter, count)
                center = (i, i + 1)
    if counter > longest and center[0] > ret[0]:
        T = "R"
        longest = counter
        ret = center

    # Column checks for even center
    counter = -1
    center = (-1, -1)
    for i in range(len(colHashes) - 1):
        count = 0
        l = i
        r = i + 1
        while l > -1 and r < len(colHashes):
            if colHashes[l] == colHashes[r]:
                count += 1
            else:
                break
            l -= 1
            r += 1
        if count > counter and (l == -1 or r == len(colHashes)):
            if TYPE == "C":
                if (i, i + 1) != innequate:
                    counter = max(counter, count)
                    center = (i, i + 1)
            else:
                counter = max(counter, count)
                center = (i, i + 1)
    if counter > longest and center[0] > ret[0]:
        T = "C"
        longest = counter
        ret = center
    return (T, ret)

def solve(_grid, innequate, TYPE):
    row_hashes = []
    col_hashes = []
    for r in range(len(_grid)):
        hash = 0
        for c in range(len(_grid[r])):
            hash += ord(_grid[r][c])
            hash *= P
            hash %= M
        row_hashes.append(hash)

    for c in range(len(_grid[0])):
        hash = 0
        for r in range(len(_grid)):
            hash += ord(_grid[r][c])
            hash *= P
            hash %= M
        col_hashes.append(hash)
    T, center = findReflection(row_hashes, col_hashes, innequate, TYPE)
    return T, center


part1 = 0
for i in range(len(grids)):
    T, center = solve(grids[i], (-1, -1), "")
    part1 += center[0] + 1 if T == "C" else 100*(center[0] + 1)
print(part1)

part2 = 0
for i in range(len(grids)):
    TYPE, original_center = solve(grids[i], (-1, -1), "")
    row_start, row_end, col_start, col_end = 0, len(grids[i]), 0, len(grids[i][0])
    def smudge(i, original_center, TYPE):
        for r in range(row_start, row_end):
            for c in range(col_start, col_end):
                new_grid = grids[i].copy()
                new_grid[r] = new_grid[r][:c] + ("." if new_grid[r][c] == "#" else "#") + new_grid[r][c + 1:]
                T, center = solve(new_grid, original_center, TYPE)
                if center != (-1, -1):
                    return (T, center)
        return (-1, (-1, -1))

    T, center = smudge(i, original_center, TYPE)
    part2 += center[0] + 1 if T == "C" else 100*(center[0] + 1)

print(part2)

