file = open("../input.txt", "r")
queries = file.read().strip().split(",")

MULT = 17
MOD = 256

def hash(sequence):
    curr = 0
    for ele in sequence:
        curr += ord(ele)
        curr *= MULT
        curr %= MOD
    return curr


part1 = 0
boxes = [[] for i in range(MOD)]
for query in queries:
    part1 += hash(query)

    if "=" in query:
        label, focal_length = query.split("=")
        box = hash(label)
        found = False
        for i in range(len(boxes[box])):
            tag, focal = boxes[box][i]
            if tag == label:
                boxes[box][i][1] = focal_length
                found = True
                break

        if not found:
            boxes[box].append([label, focal_length])
    else:
        label = query[:-1]
        box = hash(label)
        for i in range(len(boxes[box])):
            tag, focal = boxes[box][i]
            if tag == label:
                boxes[box].pop(i)
                break

part2 = 0
for i in range(MOD):
    for j in range(len(boxes[i])):
        part2 += (i + 1) * (j + 1) * (int(boxes[i][j][1]))

print(part1)
print(part2)

