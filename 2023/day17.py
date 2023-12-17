import heapq

file = open("Inputs/day17.txt", "r")
grid = [i.strip() for i in file.readlines()]

H = len(grid)
W = len(grid[0])

dr = [0, 0, -1, 1]
dc = [-1, 1, 0, 0]

def part1():
    queue = []
    queue.append((0, 0, 0, 0, 0, 0))
    # have different distances for nodes that came from the 4 different directions
    dist = {}

    while queue:
        d, r, c, dir_r, dir_c, repeats = heapq.heappop(queue)
        if r < 0 or r >= H or c < 0 or c >= W:
            continue
        if (r, c) == (H - 1, W - 1):
            break
        for i in range(len(dr)):
            if (dir_r, dir_c) == (-dr[i], -dc[i]):
                continue
            reps = 0
            if (dir_r, dir_c) == (dr[i], dc[i]):
                reps = repeats
            rr = r
            cc = c
            subtot = d
            not_good = False
            for _ in range(1):
                rr += dr[i]
                cc += dc[i]
                if rr < 0 or rr >= H or cc < 0 or cc >= W or reps >= 10:
                    not_good = True
                    break
                subtot += int(grid[rr][cc])
                reps += 1
            while reps <= 3 and not not_good:
                if (rr, cc, dr[i], dc[i], reps) in dist:
                    if subtot < dist[(rr, cc, dr[i], dc[i], reps)]:
                        dist[(rr, cc, dr[i], dc[i], reps)] = subtot
                        heapq.heappush(queue, (subtot, rr, cc, dr[i], dc[i], reps))
                else:
                    dist[(rr, cc, dr[i], dc[i], reps)] = subtot
                    heapq.heappush(queue, (subtot, rr, cc, dr[i], dc[i], reps))
                rr += dr[i]
                cc += dc[i]
                if rr < 0 or rr >= H or cc < 0 or cc >= W:
                    break
                subtot += int(grid[rr][cc])
                reps += 1

    best = []
    for r, c, ddr, ddc, reps in dist:
        if (r, c) == (H - 1, W - 1):
            best.append(dist[(r, c, ddr, ddc, reps)])
    return min(best)

def part2():
    queue = []
    queue.append((0, 0, 0, 0, 0, 0))
    # have different distances for nodes that came from the 4 different directions
    dist = {}

    while queue:
        d, r, c, dir_r, dir_c, repeats = heapq.heappop(queue)
        if r < 0 or r >= H or c < 0 or c >= W:
            continue
        if (r, c) == (H - 1, W - 1):
            break
        for i in range(len(dr)):
            if (dir_r, dir_c) == (-dr[i], -dc[i]):
                continue
            reps = 0
            if (dir_r, dir_c) == (dr[i], dc[i]):
                reps = repeats
            rr = r
            cc = c
            subtot = d
            not_good = False
            for _ in range(4):
                rr += dr[i]
                cc += dc[i]
                if rr < 0 or rr >= H or cc < 0 or cc >= W or reps >= 10:
                    not_good = True
                    break
                subtot += int(grid[rr][cc])
                reps += 1
            while reps <= 10 and not not_good:
                if (rr, cc, dr[i], dc[i], reps) in dist:
                    if subtot < dist[(rr, cc, dr[i], dc[i], reps)]:
                        dist[(rr, cc, dr[i], dc[i], reps)] = subtot
                        heapq.heappush(queue, (subtot, rr, cc, dr[i], dc[i], reps))
                else:
                    dist[(rr, cc, dr[i], dc[i], reps)] = subtot
                    heapq.heappush(queue, (subtot, rr, cc, dr[i], dc[i], reps))
                rr += dr[i]
                cc += dc[i]
                if rr < 0 or rr >= H or cc < 0 or cc >= W:
                    break
                subtot += int(grid[rr][cc])
                reps += 1

    best = []
    for r, c, ddr, ddc, reps in dist:
        if (r, c) == (H - 1, W - 1):
            best.append(dist[(r, c, ddr, ddc, reps)])
    return min(best)

print(part1())
print(part2())
