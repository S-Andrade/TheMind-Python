
list_cards = [[50],[],[50,90], [50],[99]]
list_cards0 = [[20],[],[],[60],[]]
list_cards1 = [[60],[],[10,20],[70],[90]]

for cards, cards0, cards1 in zip(list_cards,list_cards0, list_cards1):
    if len(cards) > 0 and (
        (len(cards0) > 0 and len(cards1) > 0 and (cards[0] > cards0[0] or cards[0] > cards1[0]) ) or
        (len(cards0) == 0 and len(cards1) > 0 and cards[0] > cards1[0]) or
        (len(cards1) == 0 and len(cards0) > 0 and cards[0] > cards0[0]) ):
            print(str(cards)+" "+str(cards0)+" "+str(cards1))
    
        