import re

file = open("Inputs/day12.txt", "r")
input = [i.strip().split() for i in file.readlines()]

springs = []
damaged_segments = []
for spring, damaged in input:
    springs.append(spring)
    damaged_segments.append(list(map(int, damaged.split(","))))

print(springs)
print(damaged_segments)


def equivalent(word1, word2):
    for i in range(len(word1)):
        if word1[i] != word2[i] and word1[i] != "?":
            return False
    print(word2)
    return True

def solvePart1():
    ret = 0
    for i in range(len(springs)):
        added = set()
        least_length = sum(damaged_segments[i]) + len(damaged_segments[i]) - 1
        segments = ["#" * length for length in damaged_segments[i]]
        optimal = ".".join(segments)

        print(optimal)
        extra_length = len(springs[i]) - least_length
        queue = [(extra_length, optimal)]
        while queue:
            to_add, string = queue.pop(-1)
            if to_add == 0:
                ret += equivalent(springs[i], string)
                continue

            if "." + string not in added:
                queue.append((to_add - 1, "." + string))
                added.add("." + string)
                # print(queue[-1])
            if string + "." not in added:
                queue.append((to_add - 1, string + "."))
                added.add(string + ".")
                # print(queue[-1])

            broken = False
            for j in range(len(string)):
                if string[j] == "." and broken:
                    if string[:j] + "." + string[j:] not in added:
                        queue.append((to_add - 1, string[:j] + "." + string[j:]))
                        added.add(string[:j] + "." + string[j:])
                    # print(queue[-1])
                    broken = not broken
                elif string[j] == "#" and not broken:
                    broken = not broken
    return ret

part1 = solvePart1()
print(part1)



