file = open("../input.txt", "r")
input = [i.strip() for i in file.readlines()]

# Expand empty rows and columns
rows_is_empty = [True]*len(input)
columns_is_empty = [True]*len(input[0])

for r in range(len(input)):
    if input[r].count(".") != len(input[r]):
        rows_is_empty[r] = False
    for c in range(len(input[0])):
        if input[r][c] == "#":
            columns_is_empty[c] = False

galaxies = []
for r in range(len(input)):
    for c in range(len(input[0])):
        if input[r][c] == "#":
            galaxies.append((r, c))

def quickShortedPath(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


# expanded distance =
# normal distance + number of expanded columns * (expansion rate - 1) + number of expanded rows * (expansion rate - 1)
part1 = 0
part2 = 0
part1Rate = 2 - 1
part2Rate = 10**6 - 1
for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
        start = galaxies[i]
        end = galaxies[j]

        # Find number of rows expanded in between starting galaxy and ending galaxy
        rowsExpanded = sum(rows_is_empty[min(start[0], end[0]):max(start[0], end[0]) + 1])
        # Find number of columns expanded in between starting galaxy and ending galaxy
        columnsExpanded = sum(columns_is_empty[min(start[1], end[1]):max(start[1], end[1]) + 1])
        part1 += quickShortedPath(start, end) + rowsExpanded*part1Rate + columnsExpanded*part1Rate
        part2 += quickShortedPath(start, end) + rowsExpanded*part2Rate + columnsExpanded*part2Rate

print(part1)
print(part2)

