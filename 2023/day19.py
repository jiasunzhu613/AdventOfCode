import re
file = open("../input.txt", "r")
r, v = file.read().split("\n\n")

rules = {}
rr = r.strip().split("\n")
var_map = {"x":0, "m":1, "a":2, "s": 3}
for ele in rr:
    app = []
    temp = ele[:-1]
    name, rule = temp.split("{")

    subrules = rule.split(",")
    for subrule in subrules:
        nums = re.findall("\d+", subrule)
        words = re.findall("[a-z,A-Z]+", subrule)
        found_less_than = "<" in subrule
        processed = []
        if len(words) == 1:
            processed.append(words[0])
        else:
            processed.append(var_map[words[0]])
            processed.append("<" if found_less_than else ">")
            processed.append(int(nums[0]))
            processed.append(words[1])
        app.append(processed)
    rules[name] = app

values = []
vv = v.strip().split("\n")
for ele in vv:
    vals = [int(x) for x in re.findall("\d+", ele)]
    values.append(vals)

def nirdev_ma_goat(i, rule_name):
    if rule_name == "A":
        return True
    if rule_name == "R":
        return False

    for rule in rules[rule_name]:
        if len(rule) == 1:
            return nirdev_ma_goat(i, rule[0])
        else:
            if rule[1] == "<":
                if values[i][rule[0]] < rule[2]:
                    return nirdev_ma_goat(i, rule[3])
            else:
                if values[i][rule[0]] > rule[2]:
                    return nirdev_ma_goat(i, rule[3])

part1 = 0
for i in range(len(values)):
    if nirdev_ma_goat(i, "in"):
        part1 += sum(values[i])
print(part1)

# find all paths to accepted
accepted = []
queue = []
queue.append(([], "in"))
while queue:
    path, rule_name = queue.pop(-1)
    if rule_name == "A":
        accepted.append(path)
        continue

    if rule_name == "R":
        continue

    complement_path = []
    for rule in rules[rule_name]:
        if len(rule) == 1:
            queue.append((path + complement_path, rule[0]))
        else:
            if rule[1] == "<":
                queue.append((path + [rule[:-1]] + complement_path, rule[-1]))
                complement_path.append([rule[0], ">", rule[2] - 1])
            else:
                queue.append((path + [rule[:-1]] + complement_path, rule[-1]))
                complement_path.append([rule[0], "<", rule[2] + 1])

part2 = 0
for criterions in accepted:
    nums = [[1, 4000] for _ in range(4)]
    for criterion in criterions:
        if criterion[1] == "<":
            nums[criterion[0]][1] = min(criterion[2] - 1, nums[criterion[0]][1])
        else:
            nums[criterion[0]][0] = max(criterion[2] + 1, nums[criterion[0]][0])
    temp = 1
    for lo, hi in nums:
        temp *= hi - lo + 1
    part2 += temp

print(part2)




