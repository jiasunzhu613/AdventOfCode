file = open("inputs/day2.txt", "r")
reports = [list(map(int, line.split())) for line in file.readlines()]

def check_safe(report):
    difference = []
    for i in range(len(report) - 1):
        difference.append(report[i + 1] - report[i])
    if not (all(ele < 0 for ele in difference) or all(ele > 0 for ele in difference)):
        return False
    return all(1 <= abs(ele) <= 3 for ele in difference)

part1 = 0
part2 = 0
for report in reports:
    part1 += check_safe(report)
    for i in range(len(report)):
        if check_safe(report[:i] + report[i + 1:]):
            part2 += 1
            break
print(part1)
print(part2)

