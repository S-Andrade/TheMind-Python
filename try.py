import random

def getCards(Level):
    cards = []

    if Level == 1:
        cards.append(random.randint(1, 20))
        cards.append(random.randint(50, 60))
        cards.append(random.randint(90, 100))
        random.shuffle(cards)

    elif Level == 2:
        while len(cards) < 5:
            next_card = random.randint(50, 100)
            if next_card not in cards:
                cards.append(next_card)

        b = True
        while b:
            c = cards[random.randint(0, 3)] + 2
            if c not in cards and c < 100:
                cards.append(c)
                b = False

    elif Level == 3:
        while len(cards) < 7:
            next_card = random.randint(1, 100)
            if next_card not in cards:
                cards.append(next_card)
        b = True
        while b:
            c = cards[random.randint(2, 6)] + 3
            if c not in cards and c < 100:
                cards.insert(4, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(2, 7)] + 1
            if c not in cards  and c < 100:
                cards.insert(0, c)
                b = False

    elif Level == 4:
        cards.append(1)
        e = f = g = 0
        while len(cards) < 11:
            if e < 3:
                next_card = random.randint(1, 20)
                if next_card not in cards:
                    cards.append(next_card)
                    e += 1
            if f < 3:
                next_card = random.randint(50, 70)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 4:
                next_card = random.randint(75, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(4, 6)] + 2
            if c not in cards and c < 100:
                cards.insert(7, c)
                b = False

    elif Level == 5:
        f = g = 0
        while len(cards) < 13:
            if f < 7:
                next_card = random.randint(1, 20)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 7:
                next_card = random.randint(70, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(0, 3)] + 2
            if c not in cards and c < 100:
                cards.insert(4, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(0, 9)] + 5
            if c not in cards and c < 100:
                cards.append(c)
                b = False

    elif Level == 6:
        f = g = 0
        while len(cards) < 18:
            if f < 9:
                next_card = random.randint(1, 20)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 9:
                next_card = random.randint(70, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1

    elif Level == 7:
        f = g = 0
        while len(cards) < 19:
            if f < 3:
                next_card = random.randint(1, 10)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 16:
                next_card = random.randint(40, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(0, 5)] + 2
            if c not in cards and c < 100:
                cards.insert(6, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(7, 13)] + 1
            if c not in cards and c < 100:
                cards.append(c)
                b = False

    elif Level == 8:
        e = f = g = 0
        while len(cards) < 24:
            if e < 8:
                next_card = random.randint(1, 20)
                if next_card not in cards:
                    cards.append(next_card)
                    e += 1
            if f < 8:
                next_card = random.randint(25, 40)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 8:
                next_card = random.randint(50, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1

    elif Level == 9:
        f = g = 0
        while len(cards) < 25:
            if f < 9:
                next_card = random.randint(1, 25)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 16:
                next_card = random.randint(50, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(9, 16)] + 3
            if c not in cards and c < 100:
                cards.insert(17, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(0, 8)] + 1
            if c not in cards and c < 100:
                cards.append(c)
                b = False

    elif Level == 10:
        while len(cards) < 30:
            next_card = random.randint(1, 100)
            if next_card not in cards:
                cards.append(next_card)

    print(cards)
    # Distribute cards to each player
    hands = []
    for i in range(3):
        hand = cards[i*Level : (i + 1)*Level]
        hands.append(sorted(hand))

    return hands



cards = getCards(10)
print(cards)