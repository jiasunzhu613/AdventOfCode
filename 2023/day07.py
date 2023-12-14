import functools
file = open("Inputs/day7.txt", "r")
input = [i.strip() for i in file.readlines()]

"""
Hand types:
Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
"""

# Strength mapping for compare function in part 1
strength = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")
mapping = {}
for i in range(len(strength)):
    mapping[strength[i]] = i

# Strength mapping for compare function in part 2
strengthPart2 = "A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")
mappingPart2 = {}
for i in range(len(strengthPart2)):
    mappingPart2[strengthPart2[i]] = i


# https://stackoverflow.com/questions/5213033/sort-a-list-of-lists-with-a-custom-compare-function
# Return negative value when left item should be sorted BEFORE right item
# Return positive value when left item shuold be sorted AFTER right item
# Return 0 if the two items are of equal value
def compare(item1, item2):
    # PART 1
    # for i in range(len(item1)):
    #     if mapping[item1[i]] < mapping[item2[i]]:
    #         return -1
    #     elif mapping[item1[i]] > mapping[item2[i]]:
    #         return 1
    # return 0

    # PART 2
    for i in range(len(item1)):
        if mappingPart2[item1[i]] < mappingPart2[item2[i]]:
            return -1
        elif mappingPart2[item1[i]] > mappingPart2[item2[i]]:
            return 1
    return 0

five = []
four = []
full_house = []
three = []
two_pair = []
one_pair = []
high = []

bids = {}
for i in input:
    splitted = i.split()
    card, bid = splitted[0], int(splitted[1])
    bids[card] = bid

for card in bids:
    freq = {}
    for ele in card:
        if ele not in freq:
            freq[ele] = 1
            continue
        freq[ele] += 1

    J = freq["J"] if "J" in freq else 0
    values = []
    for ele in freq:
        if ele == "J":
            continue
        values.append(freq[ele])
    if not values:
        values.append(0)
    values.sort(reverse=True)
    ind = 0
    while J > 0:
        needed = 5 - values[ind]
        values[ind] += min(J, needed)
        J -= min(J, needed)
        ind += 1

    triples = 0
    pairs = 0
    processed = False
    for val in values:
        if val == 5:
            five.append(card)
            processed = True
            break

        if val == 4:
            four.append(card)
            processed = True
            break

        if val == 3:
            triples += 1
            continue

        if val == 2:
            pairs += 1
            continue

    if triples == 1 and pairs == 1:
        full_house.append(card)
    elif triples > 0:
        three.append(card)
    elif pairs == 2:
        two_pair.append(card)
    elif pairs == 1:
        one_pair.append(card)
    elif not processed:
        high.append(card)

all_cards = [five, four, full_house, three, two_pair, one_pair, high]
for i in range(len(all_cards)):
    all_cards[i].sort(key=functools.cmp_to_key(compare))

tot = 0
multiplier = len(bids)
for card_type in all_cards:
    for card in card_type:
        tot += bids[card]*multiplier
        multiplier -= 1
print(tot)





