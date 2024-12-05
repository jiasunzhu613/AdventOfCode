import re

file = open("inputs/day3.txt", "r")

instructions = file.read().strip()

valid_commands = re.findall(r"mul\(\d+,\d+\)", instructions)
valid_commands_loc = [m.start() for m in re.finditer(r"mul\(\d+,\d+\)", instructions)]
do = [m.start() for m in re.finditer(r"do\(\)", instructions)]
dont = [m.start() for m in re.finditer(r"don't\(\)", instructions)]

# part1 = 0
# for command in valid_commands:
#     comma = command.find(",")
#     num1 = int(command[4:comma])
#     num2 = int(command[comma + 1: -1])
#     part1 += num1 * num2
# print(part1)

part2 = 0
ranges = [(0, 1)]
dont_ind = 0
for ele in do:
    while dont_ind < len(dont) and dont[dont_ind] < ele:
        ranges.append((dont[dont_ind], 0))
        dont_ind += 1
    ranges.append((ele, 1))
while dont_ind < len(dont):
    ranges.append((dont[dont_ind], 0))
    dont_ind += 1
ranges.append((float("INF"), 1))

curr = 0
for i in range(len(ranges) - 1):
    while curr < len(valid_commands_loc) and ranges[i][0] <= valid_commands_loc[curr] <= ranges[i + 1][0]:
        if ranges[i][1] != 0:
            command = valid_commands[curr]
            comma = command.find(",")
            num1 = int(command[4:comma])
            num2 = int(command[comma + 1: -1])
            part2 += num1 * num2
        curr += 1
print(part2)







