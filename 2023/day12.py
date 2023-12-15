import re, itertools, sys

file = open("../input.txt", "r")
input = [i.strip().split() for i in file.readlines()]

queries = []
# springs = []
# damaged_segments = []
for spring, damaged in input:
    queries.append((spring, list(map(int, damaged.split(",")))))
    # springs.append(spring)
    # damaged_segments.append(list(map(int, damaged.split(","))))

check_broken_memo = {}
def check_broken(spring, broken_segments):
    if (spring, broken_segments) in check_broken_memo:
        return check_broken_memo[(spring, broken_segments)]
    all_broken = " ".join(re.findall("#+", spring))

    check_broken_memo[(spring, broken_segments)] = broken_segments == all_broken
    return check_broken_memo[(spring, broken_segments)]

works_memo = {}
def works(original, created):
    if (original, created) in works_memo:
        return works_memo[(original, created)]
    works_memo[(original, created)] = all([original[i] == created[i] or original[i] == "?" for i in range(len(original))])
    return works_memo[(original, created)]

orientation_memo = {}
def get_orientations(ind, curr, spring, broken_segments, use_memo):
    if (spring, broken_segments) in orientation_memo:
        return orientation_memo[(spring, broken_segments)]
    if ind == len(spring):
        return check_broken(curr, broken_segments) and works(spring, curr)

    if spring[ind] != "?":
        if use_memo:
            orientation_memo[(spring, broken_segments)] = get_orientations(ind + 1, curr + spring[ind], spring, broken_segments, False)
            return orientation_memo[(spring, broken_segments)]
        else:
            return get_orientations(ind + 1, curr + spring[ind], spring, broken_segments, False)
    if use_memo:
        orientation_memo[(spring, broken_segments)] = get_orientations(ind + 1, curr + "#", spring, broken_segments, False) \
            + get_orientations(ind + 1, curr + ".", spring, broken_segments, False)
        return orientation_memo[(spring, broken_segments)]
    else:
        return get_orientations(ind + 1, curr + "#", spring, broken_segments, False) \
        + get_orientations(ind + 1, curr + ".", spring, broken_segments, False)


part1 = 0
ind = 0
for spring, damaged in queries:
    partials = re.findall("[?#]+", spring)
    # we will have a distribution of len(partial)
    balls = len(damaged)
    boxes = len(partials)
    rng = list(range(balls + 1)) * boxes
    distributions = list(set(i for i in itertools.permutations(rng, boxes) if sum(i) == balls))
    print(ind)
    ind += 1
    for i in range(len(distributions)):
        subtotal = 0
        for j in range(len(distributions[i])):
            partial_damaged = damaged[0 if j == 0 else distributions[i][j-1] : distributions[i][j]]
            subtotal += get_orientations(0, "", spring, " ".join(["#" * i for i in partial_damaged]), True)

print(part1)


