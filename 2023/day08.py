import re, math
file = open("../input.txt", "r")
instructions, temp = [i.strip() for i in file.read().split("\n\n")]

nodes = [i.strip() for i in temp.split("\n")]
network = {}

endingA = []
for node in nodes:
    eles = list(re.findall("\w+", node))
    if eles[0][-1] == "A":
        endingA.append(eles[0])
    dest = (eles[1], eles[2])
    network[eles[0]] = dest

# Get # of steps needs for each node that ends with "A" to end with "Z"
def get_count(val):
    count = 0
    ind = 0
    curr = val
    while curr[-1] != "Z":
        if ind >= len(instructions):
            ind = 0

        curr = network[curr][0 if instructions[ind] == "L" else 1]
        ind += 1
        count += 1
    return count

# Find all steps needed for each element
count_needed = [get_count(ele) for ele in endingA]

# REMEMBER!! THERE IS BUILT IN LCM IN MATH MODULE!!!!
# def lcm(a, b):
#     return (a * b) // math.gcd(a, b)

# Find lowest common multiple of all the step counts for each node that was processed!
total_steps = count_needed[0]
for i in range(1, len(count_needed)):
    total_steps = math.lcm(total_steps, count_needed[i])
print(total_steps)
