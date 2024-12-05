file = open("../input.txt", "r")
input = [i.strip() for i in file.readlines()]

bricks = []
for brick in input:
    start, end = brick.split("~")
    start = list(map(int, start.split(",")))
    end = list(map(int, end.split(",")))
    temp = []
    temp.append(start)
    temp.append(end)
    if start == end:
        temp.append(0)
    else:
        for i in range(3):
            if start[i] != end[i]:
                temp.append(i)
                break
    bricks.append(temp)






