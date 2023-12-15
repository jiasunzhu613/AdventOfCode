import re, itertools, sys
sys.setrecursionlimit(10**5)

file = open("../input.txt", "r")
input = [i.strip().split() for i in file.readlines()]

springs = []
damaged_segments = []
for spring, damaged in input:
    springs.append(spring)
    damaged_segments.append(list(map(int, damaged.split(","))))

# IDEAS:
# for each index of broken springs
# split the needed orientation with ?'s by . then solve each component and multiply eachother together
def equivalent(word1, word2):
    if len(word1) != len(word2):
        return False
    for i in range(len(word1)):
        if word1[i] != word2[i] and word1[i] != "?":
            return False
    # print(word2)
    return True

memo = {}
def helper(to_add, ind, segment, optimal):  # solves number of orientations for a small segment
    global memo
    # print((to_add, segment, optimal))
    if len(optimal) > len(segment):
        return 0
    if (to_add, ind, optimal) in memo:
        return memo[(to_add, ind, optimal)]
    if ind == len(segment):
        return 0
    if to_add == 0:
        return equivalent(segment, optimal)

    new_add = optimal[:ind] + "." + optimal[ind:]
    add = helper(to_add - 1, ind + 1, segment, new_add)
    dont = helper(to_add, ind + 1, segment, optimal)
    total = add + dont

    if (to_add, ind, optimal) not in memo:
        memo[(to_add, ind, optimal)] = total
    return memo[(to_add, ind, optimal)]

def naive(segments, distribution, broken_segments):
    distribution = [0] + distribution
    segments = [""] + segments
    ret = 1
    for i in range(1, len(segments)):
        needed = [] # build optimal from distribution
        start = sum(distribution[:i])
        for j in range(start, start + distribution[i]):
            needed.append("#" * broken_segments[j])
        optimal = ".".join(needed)
        # print(len(segments[i]) - len(optimal), segments[i], optimal)
        ret *= helper(len(segments[i]) - len(optimal), 0, segments[i], optimal)
    return ret


def solve(spring, broken_segment):
    segments = re.findall("[#?]+", spring)
    # FOR EACH SEGMENT, SOLVE FOR NUMBER OF ORIENTATIONS
    orientations = 0
    # check all ways broken segments can be fitted into each segment of the spring
    # first build a distribution of the broken segments
    balls = len(broken_segment)
    boxes = len(segments)
    rng = list(range(balls + 1)) * boxes
    distributions = list(set(i for i in itertools.permutations(rng, boxes) if sum(i) == balls))
    print(distributions)
    for i in range(len(distributions)):
        orientations += naive(segments, list(distributions[i]), broken_segment)
    return orientations


part1 = 0
part2 = 0
L = len(springs)
for i in range(L):
    print("processing", i)
    # solve for total number of working orientations
    # part2 += solve("?".join([springs[i]] * 5), damaged_segments[i] * 5)
    part1 += solve(springs[i], damaged_segments[i])

print(part1)

# optimal = ".".join(["#" * i for i in damaged_segments[0]])
# print(helper(len(springs[0]) - len(optimal), springs[0], optimal, set()))
