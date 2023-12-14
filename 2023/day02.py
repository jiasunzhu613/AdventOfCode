file = open("Inputs/day2.txt", "r")
input = [i.strip().split(":") for i in file.readlines()] # add 1 to each index later


# PROCESS INPUT
games = [(0, 0)]
for i in range(len(input)):
    game, grabs = input[i]
    grabs.strip()
    separated_grabs = grabs.split("; ")
    process_game = []
    for j in range(len(separated_grabs)):
        grab = separated_grabs[j].split(", ")
        # 0 -> red, 1 -> green, 2 -> blue
        colours = [0, 0, 0]
        for cube in grab:
            num, colour = cube.split()
            assert(colour == "red" or colour == "blue" or colour == "green")
            if colour == "red":
                colours[0] = int(num)
            if colour == "green":
                colours[1] = int(num)
            if colour == "blue":
                colours[2] = int(num)
        process_game.append(colours)
    games.append((i + 1, process_game))

tot = 0
for game, grabs in games:
    if game == 0:
        continue
    max_cubes = [0, 0, 0]
    for grab in grabs:
        for i in range(len(grab)):
            max_cubes[i] = max(max_cubes[i], grab[i])
    # PART 1
    # if max_cubes[0] <= 12 and max_cubes[1] <= 13 and max_cubes[2] <= 14:
    #     tot += game

    # PART 2
    tot += max_cubes[0] * max_cubes[1] * max_cubes[2]

print(tot)


