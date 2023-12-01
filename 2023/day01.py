file = open("../input.txt", "r")
input = [i.strip() for i in file.readlines()]

tot = 0
valid = ["zero", "one", "two", "three", "four", "five", "six", "seven",
         "eight", "nine",
         "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
process = {}
for i in range(10):
    process[valid[i]] = str(i)
for code in input:
    # FIND FIRST AND LAST NUMBER
    first = ""
    first_ind = float("INF")
    for val in valid:
        index = code.find(val)
        if index == -1:
            continue
        if index < first_ind:
            first_ind = index
            if val in process:
                first = process[val]
            else:
                first = val

    last = ""
    last_ind = -1
    for val in valid:
        all_indices = []
        temp = code
        erased = 0
        # Find all copies of a value in the code (part 2)
        while temp:
            index = temp.find(val)
            if index == -1:
                break
            all_indices.append(index + len(val) - 1 + erased)
            temp = temp[index + len(val):]
            erased += index + len(val)
        if not all_indices:
            continue
        index = max(all_indices)
        if index > last_ind:
            last_ind = index
            if val in process:
                last = process[val]
            else:
                last = val
    num = first + last
    tot += int(num)

print(tot)

