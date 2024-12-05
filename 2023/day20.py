file = open("../input.txt", "r")
input = [i.strip() for i in file.readlines()]

wire_type = {}
paths = {}

for line in input:
    if "broadcaster" in line:
        source, temp_dest = line.split(" -> ")
        destinations = temp_dest.split(", ")
        paths[source] = destinations
        continue

    t = line[0]
    source, temp_dest = line[1:].split(" -> ")
    destinations = temp_dest.split(", ")

    wire_type[source] = t
    paths[source] = destinations

print(wire_type)
print(paths)

# check cycles
"""
rules:
flip flop: 
- high doesnt do anything
- low flip-flops the on/off (initially off)

conjunction:
- sends opposing charge to what was received

if there is no cycle, press buton again, if there is a cycle just go by that?
"""







