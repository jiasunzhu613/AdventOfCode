file = open("inputs/day1.txt", "r")

left, right = [], []
for line in file.readlines():
    a, b = map(int, line.split())
    left.append(a)
    right.append(b)

left.sort()
right.sort()
part1 = sum(abs(left[i] - right[i]) for i in range(len(left)))
print(part1)

rank = 0
mapping = {}
for ele in left:
    if ele not in mapping:
        mapping[ele] = rank
        rank += 1

freq = [0] * len(mapping)
for ele in right:
    if ele in mapping:
        freq[mapping[ele]] += 1

part2 = sum(freq[mapping[ele]] * ele for ele in left)
print(part2)


