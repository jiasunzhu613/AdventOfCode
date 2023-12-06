file = open("../input.txt", "r")
input = [i.strip() for i in file.readlines()]
# store different maps in array
seeds = list(map(int, input[0].split(": ")[1].split()))
part2_seeds = []
for i in range(0, len(seeds), 2):
    part2_seeds.append((seeds[i], seeds[i + 1]))
maps = []
# upon encountering blank
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
# print(maps)
# part1 = float("INF")
# for seed in seeds:
#     curr = seed
#     for i in range(len(maps)):
#         for dest, source, length in maps[i]:
#             if source <= curr < source + length:
#                 length_away = curr - source
#                 curr = dest + length_away
#                 break
#     if curr < part1:
#         part1 = curr
# print(part1)

# part2 = float("INF")
# # count ranges of maps instead of seeds
# for seed_start, length_seed in part2_seeds:
#     seed_end = seed_start + length_seed
#     for seed in range(seed_start, seed_end):
#         curr = seed
#         for i in range(len(maps)):
#             for dest, source, length in maps[i]:
#                 if source <= curr < source + length:
#                     length_away = curr - source
#                     curr = dest + length_away
#                     break
#             print(seed, curr)
#         if curr < part2:
#             part2 = curr
#     print()
# print()
# print(part2)

# implementation idea:
# find smallest values in ranges that fit into a map or can be mapped to
# adding extra values only increases the value
# case 1: all of a range fit
# case 2: start of range fits, but back doesnt
# case 3: end of range fits, but not start
memo = {}
def solve(start, end, ind):
    # print(ind, start, end)
    if start == 0:
        print(start, end, ind)
    if end < start:
        return float("INF")
    if ind == len(maps) - 1:
        return start
    if (start, end, ind) in memo:
        return memo[(start, end, ind)]
    # find start point of map
    val = float("INF")

    for dest, source, length in maps[ind]:
        end_source = source + length - 1
        end_dest = dest + length - 1
        # null cases

        # completely covered cases
        if start <= source <= end_source <= end:
            # val = min(val, solve(dest, end_dest, ind + 1))
            temp_source = source - 1
            temp_end_source = end_source + 1
            val = min(val, min(solve(dest, end_dest, ind + 1), solve(start, temp_source, ind + 1), solve(temp_end_source, end, ind + 1)))
        elif source <= start <= end <= end_source:

            front_buffer = start - source
            back_buffer = end_source - end
            val = min(val, solve(dest + front_buffer, end_dest - back_buffer, ind + 1))

        # front covered but back not case
        elif start <= source <= end <= end_source:
            distance_from_end = end - source
            # val = min(val, solve(dest, dest + distance_from_end, ind + 1))
            temp_source = source - 1
            val = min(val, min(solve(dest, dest + distance_from_end, ind + 1), solve(start, temp_source, ind + 1)))

        # back covered but front not case
        elif source <= start <= end_source <= end:
            distance_to_front = start - source
            # val = min(val, solve(dest + distance_to_front, end_dest, ind + 1))
            temp_end_source = end_source + 1
            val = min(val, min(solve(dest + distance_to_front, end_dest, ind + 1), solve(temp_end_source, end, ind + 1)))

    val = min(val, solve(start, end, ind + 1))
    if (start, end, ind) not in memo:
        memo[(start, end, ind)] = val
    return memo[(start, end, ind)]

part2 = float("INF")
for seed_start, length_seed in part2_seeds:
    seed_end = seed_start + length_seed - 1
    part2 = min(part2, solve(seed_start, seed_end, 1))
    print(part2)
print(part2)
# print(solve(part2_seeds[0][0], part2_seeds[0][0] + part2_seeds[0][1] - 1, 1))
# print()
# print(solve(part2_seeds[1][0], part2_seeds[1][0] + part2_seeds[1][1] - 1, 1))
# print(solve(82, 82, 1))




"""
79 79
79 81
79 81
79 81
79 74
79 78
79 78
79 82
80 80
80 82
80 82
80 82
80 75
80 79
80 79
80 83
81 81
81 83
81 83
81 83
81 76
81 80
81 80
81 84
82 82 -> here!
82 84
82 84
82 84
82 77
82 45
82 46
82 46
83 83
83 85
83 85
83 85
83 78
83 46
83 47
83 47
84 84
84 86
84 86
84 86
84 79
84 47
84 48
84 48
85 85
85 87
85 87
85 87
85 80
85 48
85 49
85 49
86 86
86 88
86 88
86 88
86 81
86 49
86 50
86 50
87 87
87 89
87 89
87 89
87 82
87 50
87 51
87 51
88 88
88 90
88 90
88 90
88 83
88 51
88 52
88 52
89 89
89 91
89 91
89 91
89 84
89 52
89 53
89 53
90 90
90 92
90 92
90 92
90 85
90 53
90 54
90 54
91 91
91 93
91 93
91 93
91 86
91 54
91 55
91 55
92 92
92 94
92 94
92 94
92 87
92 55
92 56
92 60
93 93
93 95
93 95
93 95
93 95
93 63
93 64
93 68

55 55
55 57
55 57
55 53
55 46
55 82
55 82
55 86
56 56
56 58
56 58
56 54
56 47
56 83
56 83
56 87
57 57
57 59
57 59
57 55
57 48
57 84
57 84
57 88
58 58
58 60
58 60
58 56
58 49
58 85
58 85
58 89
59 59
59 61
59 61
59 61
59 54
59 90
59 90
59 94
60 60
60 62
60 62
60 62
60 55
60 91
60 91
60 95
61 61
61 63
61 63
61 63
61 56
61 92
61 92
61 96
62 62
62 64
62 64
62 64
62 57
62 93
62 93
62 56
63 63
63 65
63 65
63 65
63 58
63 94
63 94
63 57
64 64
64 66
64 66
64 66
64 59
64 95
64 95
64 58
65 65
65 67
65 67
65 67
65 60
65 96
65 96
65 59
66 66
66 68
66 68
66 68
66 61
66 97
66 97
66 97
67 67
67 69
67 69
67 69
67 62
67 98
67 98
67 98
68 68
68 70
68 70
68 70
68 63
68 99
68 99
68 99
"""











