file = open("Inputs/day9.txt", "r")
histories = [list(map(int, i.strip().split())) for i in file.readlines()]

part1 = 0
part2 = 0
for history in histories:
    end_values = [history[-1]]
    start_values = [history[0]]
    differences = history

    while differences.count(differences[0]) != len(differences):
        new_differences = []
        for i in range(len(differences) - 1):
            new_differences.append(differences[i + 1] - differences[i])
        differences = new_differences
        end_values.append(differences[-1])
        start_values.append(differences[0])

    # Sum up endvalues for part 1
    part1 += sum(end_values)

    # Subtract each term by the term in front of it and then take the first term as the value to add
    for i in range(len(start_values) - 2, -1, -1):
        start_values[i] -= start_values[i + 1]
    part2 += start_values[0]

print(part1)
print(part2)

