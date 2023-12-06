import math
file = open("../input.txt", "r")
input = [i.strip() for i in file.readlines()]

durations = list(map(int, input[0].split(": ")[1].split()))
records = list(map(int, input[1].split(": ")[1].split()))
# print(durations)
# print(records)

# MAIN LOGIC / SIMPLE MATH:
# D(x), represents the distance car travels by holding down button for x ms
# holding down 1 second allows us to travel 1(t - 1) mm -> x(t-x) -> tx - x^2 -> -x^2 + tx - R = 0

# PART 1
part1 = [] # number of ways to win for each race
for i in range(len(durations)):
    a = -1
    b = durations[i]
    c = -records[i]
    # x = (-b +- sqrt(b^2 - 4ac)) / 2a
    discrim = b**2 - 4*a*c
    if discrim < 0:
        part1.append(0)
        continue

    sqrt_val = discrim**0.5
    x1 = math.ceil((-b + sqrt_val) / (2*a))
    x2 = math.floor((-b - sqrt_val) / (2*a))
    part1.append(x2 - x1 + 1)

part1_tot = 1
for ele in part1:
    part1_tot *= ele
print(part1_tot)


# PART 2
duration = int("".join(map(str, durations)))
record = int("".join(map(str, records)))

part2_tot = 0
a = -1
b = duration
c = -record
# x = (-b +- sqrt(b^2 - 4ac)) / 2a
discrim = b**2 - 4*a*c
if discrim >= 0:
    sqrt_val = discrim**0.5
    x1 = math.ceil((-b + sqrt_val) / (2*a))
    x2 = math.floor((-b - sqrt_val) / (2*a))
    part2_tot = x2 - x1 + 1

print(part2_tot)

"""
WOW... 
What a change from day 5, kinda thankful tho lol after the disastrous day 5
"""




