file = open("../input.txt", "r")
input = [i.strip() for i in file.readlines()]

cards = []
for i in input:
    game, card = i.split(": ")
    card.strip()
    winning, hand = card.split(" | ")
    winning_set = set(map(int, winning.split()))
    hand_list = list(map(int, hand.split()))
    cards.append((winning_set, hand_list))

### PART 1 ###
part1 = 0
for winning_set, hand_list in cards:
    count_winning = 0
    for card in hand_list:
        if card in winning_set:
            count_winning += 1
    if count_winning >= 1:
        part1 += 2**(count_winning - 1)

print(part1)


### PART 2 ###
memo = {}
def solve(card_ind):
    count_winning = 0
    for card in cards[card_ind][1]:
        if card in cards[card_ind][0]:
            count_winning += 1
    if count_winning == 0: # base case
        return 1
    if card_ind in memo:
        return memo[card_ind]
    tot = 1
    for i in range(card_ind + 1, card_ind + count_winning + 1):
        tot += solve(i)
    if card_ind not in memo:
        memo[card_ind] = tot
    return memo[card_ind]

part2 = 0
for i in range(len(cards)):
    part2 += solve(i)

print(part2)

"""
COMMENTS: 
- wow day 4 aoc already recursion/kinda memoization dp (prolly isn't necessary)?? damn...
"""

