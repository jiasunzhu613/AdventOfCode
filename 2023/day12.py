file = open("Inputs/day12.txt", "r")
input = [i.strip().split() for i in file.readlines()]


# All ideas/a lot of implementation is not my own,
# they came from https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day12p2.py

# Main ideas:
# - Still kinda maintaining this "powerset" idea, but instead of start from nothing and building up
# using a powerset, we could start from the original spring and slowly remove from the spring
memo = {}
def solve(condition, nums):
    # base case: condition has nothing left and nums has nothing left
    if not condition:
        return 1 if not nums else 0

    if not nums:
        return 1 if "#" not in condition else 0

    if (condition, nums) in memo:
        return memo[(condition, nums)]

    ret = 0
    if condition[0] in ".?":
        ret += solve(condition[1:], nums)
    if condition[0] in "#?":
        # cases where we do not want to use this in an entire segment of broken things
        # if nums[0] == len(condition):
        #     print(condition, nums[0])
        if nums[0] <= len(condition) and "." not in condition[:nums[0]] and (nums[0] == len(condition) or condition[nums[0]] != "#"):
            ret += solve(condition[nums[0] + 1:], nums[1:])

    memo[(condition, nums)] = ret
    return memo[(condition, nums)]

part1 = 0
part2 = 0
for spring, nums in input:
    nums = tuple(map(int, nums.split(",")))
    part1 += solve(spring, nums)
    part2 += solve("?".join([spring] * 5), nums * 5)

print(part1)
print(part2)


