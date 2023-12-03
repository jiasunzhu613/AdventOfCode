file = open("../input.txt", "r")
input = [i.strip() for i in file.readlines()]

dr = [-1, -1, -1, 0, 1, 1, 1, 0]
dc = [-1, 0, 1, 1, 1, 0, -1, -1]
visited = set()
tot = 0
for r in range(len(input)):
    for c in range(len(input[r])):
        # PART 1
        # if input[r][c] != "." and not input[r][c].isalnum():
        #     for i in range(len(dr)):
        #         rr = r + dr[i]
        #         cc = c + dc[i]
        #         if (rr, cc) in visited:
        #             continue
        #         if rr < 0 or rr >= len(input) or cc < 0 or cc >= len(input[r]) or not input[rr][cc].isdigit():
        #             continue
        #         visited.add((rr, cc))
        #         number = input[rr][cc]
        #         # add digits to the left
        #         left = cc - 1
        #         while input[rr][left].isdigit():
        #             number = input[rr][left] + number
        #             visited.add((rr, left))
        #             left -= 1
        #             if left < 0:
        #                 break
        #         # add digits to the right
        #         right = cc + 1
        #         while input[rr][right].isdigit():
        #             number += input[rr][right]
        #             visited.add((rr, right))
        #             right += 1
        #             if right >= len(input[r]):
        #                 break
        #         tot += int(number)
        # PART 2
        if input[r][c] == "*":
            count = 0
            subtot = 1
            for i in range(len(dr)):
                rr = r + dr[i]
                cc = c + dc[i]
                if (rr, cc) in visited:
                    continue
                if rr < 0 or rr >= len(input) or cc < 0 or cc >= len(input[r]) or not input[rr][cc].isdigit():
                    continue
                visited.add((rr, cc))
                number = input[rr][cc]
                # add digits to the left
                left = cc - 1
                while input[rr][left].isdigit():
                    number = input[rr][left] + number
                    visited.add((rr, left))
                    left -= 1
                    if left < 0:
                        break
                # add digits to the right
                right = cc + 1
                while input[rr][right].isdigit():
                    number += input[rr][right]
                    visited.add((rr, right))
                    right += 1
                    if right >= len(input[r]):
                        break

                count += 1
                subtot *= int(number)

            if count == 2:
                tot += subtot
print(tot)
