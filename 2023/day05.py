file = open("Inputs/day5.txt", "r")
input = [i.strip() for i in file.readlines()]
# store different maps in array
seeds = list(map(int, input[0].split(": ")[1].split()))
part2_seeds = []
for i in range(0, len(seeds), 2):
    part2_seeds.append((seeds[i], seeds[i + 1]))
maps = []
# upon encountering blank, continue
temp_map = []
for i in range(1, len(input)):
    if input[i] == "":
        continue
    if input[i].find("map") != -1:
        maps.append(temp_map)
        temp_map = []
        continue

    vals = list(map(int, input[i].split()))
    temp_map.append(vals)
maps.append(temp_map)

# PART 1
part1 = float("INF")
for seed in seeds:
    curr = seed
    for i in range(len(maps)):
        for dest, source, length in maps[i]:
            if source <= curr < source + length:
                length_away = curr - source
                curr = dest + length_away
                break
    if curr < part1:
        part1 = curr
print(part1)

# PART 2
# implementation idea for part 2, start form lowest final location value and check if a value works!
def part2():
    LO = 0
    HI = 10**10
    change = False
    for i in range(1000):
        # KEY TAKEAWAY:
        # - Observing that we could work backwards from an ending location value to an initial seed value
        # - changing direction of binary search manually (although it is scuffed)
        def helper(loo, hii, switch):
            lo = loo
            hi = hii
            while lo <= hi:
                location = (lo + hi) // 2
                curr = location
                for i in range(len(maps) - 1, -1, -1):
                    for source, dest, length in maps[i]:
                        if source <= curr < source + length:
                            length_away = curr - source
                            curr = dest + length_away
                            break
                for seed_start, length in part2_seeds:
                    if seed_start <= curr <= seed_start + length - 1:
                        return location
                else:
                    if switch:
                        hi = location - 1
                    else:
                        lo = location + 1
            return -1
        # CHANGE DIRECTION OF BINARY SEARCH
        ret = helper(LO, HI, change)
        if ret == -1:
            change = not change
        else:
            HI = ret
    return HI

print(part2())