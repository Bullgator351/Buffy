
#Hero
#Villain
#BigBad/tactic
#Potential Slayer
#Wound
#Bystander

def villainDeck():
    return shared.piles['Villain Deck']

def addVillain(group=None, x=0, y=0):
    mute()
    tablePilex = VillainDeckx
    tablePiley = VillainDecky
    nextCardToMove(villainDeck(), x, y, False)

def heroDeck():
    return shared.piles['Hero Deck']

def addHero(group=None, x=0, y=0):
    mute()
    tablePilex = HeroDeckx
    tablePiley = HeroDecky
    nextCardToMove(heroDeck(), x, y, False)

def BigBad():
    return shared.piles['BigBad_Pile']

def addBigBad(group=None, x=0, y=0):
    mute()
    tablePilex = BigBadx
    tablePiley = BigBady
    nextCardToMove(BigBad(), x, y, False)

def potentialSlayers():
    return shared.piles['Potential_Slayers']

def addPotential(group=None, x=0, y=0):
    mute()
    tablePilex = Potentialx
    tablePiley = Potentialy
    nextCardToMove(potentialSlayers(), x, y, False)

def Wounds():
    return shared.piles['Wounds']

def addWound(group=None, x=0, y=0):
    mute()
    tablePilex = Woundsx
    tablePiley = Woundsy
    nextCardToMove(Wounds(), x, y, False)

def Bystanders():
    return shared.piles['Bystanders']

def addBystander(group=None, x=0, y=0):
    mute()
    tablePilex = Bystandersx
    tablePiley = Bystandersy
    nextCardToMove(Bystanders(), x, y, False)

def nextCardToMove(group, x, y, facedown, who=me):
    mute()

    if group.controller != me:
        remoteCall(group.controller, "nextCardToMove", [group, x, y, facedown, me]
        return

    if len(group) == 0:
        notify("None Left")
        return
    
    card = group.top()
    if x == 0 and y == 0:
        addToTablePile(card, facedown, who)

def addToTablePile(card, facedown=False, who=me):
    card.movetoTable(tablePilex, tablePiley, facedown)
    notify("{} adds {} to the table.".format(who, card)

