import time
import re

DarkLightToken = ("DarkLightToken", "252af8c6-f383-46f9-ae8b-f2f302bdf6b0")
CourageToken = ("CourageToken", "c5be15ab-f1a6-442c-aba1-c64ccc14961b")
# 
# These variables need to be identical to those specified in the <gameboards> and <card> sections of definition.xml
# Project for the future would be to set all the variables in definition.xml:
# BoardWidth = Gameboard.width
# BoardStartx = Gameboard.x
# BoardStarty = Gameboard.y
# CardWidth = Card.width
# CardHeight = Card.height
# 
# For now we'll set their values here:
# I found it's less confusing to deal with all the x's then all the y's
# Playmat dimensions:
BoardWidth = 1620
BoardStartx = 0 - (BoardWidth / 2)
# Width of Margin at the left end of the playmat:
BoardMarginHoriz = 26
# Width of standard card:
CardWidth = 126
# Width of box each pile goes in:
BoxWidth = 150
# Width of margin around cards inside each box:
BoxMarginHoriz = 12
# Horiz distance between boxes:
BoxSepWidth = 40
# X coordinates to place a card in the proper box:
FirstColumnx = BoardStartx + BoardMarginHoriz
SecondColumnx = FirstColumnx + BoxWidth + BoxSepWidth
ThirdColumnx = SecondColumnx + BoxWidth + BoxSepWidth
FourthColumnx = BoardStartx + 1060 + BoxMarginHoriz
FifthColumnx = FourthColumnx + BoxWidth + BoxSepWidth

# Here are the y's
BoardHeight = 836
BoardStarty = -100 - (BoardHeight / 2)
# Height of each card
CardHeight = 176
# Height of the box each pile goes in
BoxHeight = 208
# Height of margin at the top of the playmat
BoardMarginVert = 64
# Height of the space between the boxes
UpperBoxSepHeight = 56
LowerBoxSepHeight = 64
# Amount of space between each card edge and border of box
BoxMarginVert = 16

# Y coordinates of each row
FirstRowy = BoardStarty + BoardMarginVert
SecondRowy = FirstRowy + BoxHeight + UpperBoxSepHeight
ThirdRowy = SecondRowy + BoxHeight + LowerBoxSepHeight
# Sunnydale sizes
Sunnydale0x = BoardStartx + BoardMarginHoriz + (2 * BoxWidth) + (2 * BoxSepWidth)
Sunnydale0y = BoardStarty + 340
SunnydaleHeight = 182
SunnydaleWidth = 160
# Left border of each Sunnydale additional box
Sunnydale1x = Sunnydale0x + SunnydaleWidth
Sunnydale2x = Sunnydale1x + SunnydaleWidth
Sunnydale3x = Sunnydale2x + SunnydaleWidth
Sunnydale4x = Sunnydale3x + SunnydaleWidth
# Library Sizes
Library0x = BoardStartx + BoardMarginHoriz + (2 * BoxWidth) + (2 * BoxSepWidth)
Library0y = BoardStarty + 612
LibraryHeight = 200
LibraryWidth = 160
# Left border of each Library additional box
Library1x = Library0x + LibraryWidth
Library2x = Library1x + LibraryWidth
Library3x = Library2x + LibraryWidth
Library4x = Library3x + LibraryWidth
# Location of piles
Twistsx = FirstColumnx + BoxMarginHoriz
Twistsy = FirstRowy + BoxMarginVert
Strikesx = FirstColumnx + BoxMarginHoriz
Strikesy = SecondRowy + BoxMarginVert
Couragex = FirstColumnx + BoxMarginHoriz
Couragey = ThirdRowy + BoxMarginVert
Schemex = SecondColumnx + BoxMarginHoriz
Schemey = FirstRowy + BoxMarginVert
BigBadx = SecondColumnx + BoxMarginHoriz
BigBady = SecondRowy + BoxMarginVert
Potentialx = SecondColumnx + BoxMarginHoriz
Potentialy = ThirdRowy + BoxMarginVert
Escapedx = ThirdColumnx + BoxMarginHoriz
Escapedy = FirstRowy + BoxMarginVert
Woundsx = FourthColumnx + BoxMarginHoriz
Woundsy = FirstRowy + BoxMarginVert
Bystandersx = FifthColumnx + BoxMarginHoriz
Bystandersy = FirstRowy + BoxMarginVert
VillainDeckx = FifthColumnx + BoxMarginHoriz
VillainDecky = SecondRowy + BoxMarginVert
HeroDeckx = FifthColumnx + BoxMarginHoriz
HeroDecky = ThirdRowy + BoxMarginVert
#
# To do list:
#             - Automatically shuffle discard pile back into deck when draw many > cards left in deck
#             - Hotkey control of position of Dark/Light token and update number in global summary
#             - Place new villains and heroes into empty slot in Sunnydale/Library
#             - Automatically bump villains down a spot to make room for new villain
#                 and if appropriate trigger escape
#             - Automatically update victory point tally in player summary
#             - Currently the default (double-click) card action sends card to player victory pile and del sends card to player discard pile
#                 Would like to have del do one or the other depending on card.type, then use default to play card from hand
#
#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------
def moveCard(model, x, y):
    for c in table:
        if c.model == model:
            c.moveToTable(x, y)
            return c
    return table.create(model, x, y)

def createDarkLightToken(group, x=0, y=0):
    mute()
    x = BoardStartx + 1490
    y = BoardStarty + 450
    table.create("252af8c6-f383-46f9-ae8b-f2f302bdf6b0", x, y, quantity = 1, persist = False)

def createCourageToken(group, x=0, y=0):
    mute()
    x = BoardStartx + 88
    y = BoardStarty + 683
    table.create("c5be15ab-f1a6-442c-aba1-c64ccc14961b", x, y, quantity = 20, persist = False)

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))
        
def randomNumber(group, x=0, y=0):
    mute()
    max = askInteger("Random number range (1 to ....)", 6)
    if max == None: return
    notify("{} randomly selects {} (1 to {})".format(me, rnd(1,max), max))
 
def villainDeck():
    return shared.piles['Villain Deck'] 

def addVillain(group=None, x=0, y=0):
    nextVillain(villainDeck(), x, y, False)

def nextVillain(group, x, y, facedown, who=me):
    mute()

    if group.controller != me:
        remoteCall(group.controller, "nextVillain", [group, x, y, facedown, me])
        return
        
    if len(group) == 0:
        notify("HAL9000 voice: I'm afraid I can't let you do that, Dave.")
        return
        
    card = group.top()
    if x == 0 and y == 0:
        addToSunnydale(card, facedown, who)

def addToSunnydale(card, facedown=False, who=me):
    card.moveToTable(VillainDeckx, VillainDecky, facedown)            
    notify("A new villain is chillin' in Sunnydale: '{}'.".format(card))

def heroDeck():
    return shared.piles['Hero Deck'] 

def addHero(group=None, x=0, y=0):
    nextHero(heroDeck(), x, y, False)
        
def nextHero(group, x, y, facedown, who=me):
    mute()

    if group.controller != me:
        remoteCall(group.controller, "nextHero", [group, x, y, facedown, me])
        return
        
    if len(group) == 0:
        notify("HAL9000 voice: I'm afraid I can't let you do that, Dave.")
        return
        
    card = group.top()
    if x == 0 and y == 0:
        addToLibrary(card, facedown, who)        

def addToLibrary(card, facedown=False, who=me):
    card.moveToTable(HeroDeckx, HeroDecky, facedown)            
    notify("A new Hero gonna appearo in the Library: '{}'.".format(card))

def BigBad():
    return shared.piles['BigBad_Pile']
    
def addBigBad(group=None, x=0, y=0):
    nextBigBad(BigBad(), x, y, False)

def nextBigBad(group, x, y, facedown, who=me):
    mute()
    
    if group.controller != me:
        remoteCall(group.controller, "nextBigBad", [group, x, y, facedown, me])
        return

    if len(group) == 0:
        notify("WOOHOO! YOU'VE WON THE GAME!")
        return
    
    card = group.top()
    if x == 0 and y == 0:
        addToBigBad(card, facedown, who)
        
def addToBigBad(card, facedown=False, who=me):
    card.moveToTable(BigBadx, BigBady, facedown)

def potentialSlayers():
    return shared.piles['Potential_Slayers']

def addPotential(group=None, x=0, y=0):
    nextPotential(potentialSlayers(), x, y, False)
    
def nextPotential(group, x, y, facedown, who=me):
    mute()
    
    if group.controller != me:
        remoteCall(group.controller, "nextPotential", [group, x, y, facedown, me])
        return

    if len(group) == 0:
        notify("HAL9000 voice: I'm afraid I can't let you do that, Dave.")
        return
    
    card = group.top()
    if x == 0 and y == 0:
        addToPotential(card, facedown, who)

def addToPotential(card, facedown=False, who=me):
    card.moveToTable(Potentialx, Potentialy, facedown)
    
def Wounds():
    return shared.piles['Wounds']

def addWound(group=None, x=0, y=0):
    nextWound(Wounds(), x, y, False)
    
def nextWound(group, x, y, facedown, who=me):
    mute()

    if group.controller != me:
        remoteCall(group.controller, "nextWound", [group, x, y, facedown, me])
        return

    if len(group) == 0:
        notify("HAL9000 voice: I'm afraid I can't let you do that, Dave.")
        return
    
    card = group.top()
    if x == 0 and y == 0:
        addToWounds(card, facedown, who)

def addToWounds(card, facedown=False, who=me):
    card.moveToTable(Woundsx, Woundsy, facedown)

def Bystanders():
    return shared.piles['Bystanders']

def addBystander(group=None, x=0, y=0):
    nextBystander(Bystanders(), x, y, False)
    
def nextBystander(group, x, y, facedown, who=me):
    mute()
    
    if group.controller != me:
        remoteCall(group.controller, "nextBystander", [group, x, y, facedown, me])
        return

    if len(group) == 0:
        notify("HAL9000 voice: I'm afraid I can't let you do that, Dave.")
        return
    
    card = group.top()
    if x == 0 and y == 0:
        addToBystanders(card, facedown, who)

def addToBystanders(card, facedown=True, who=me):
    card.moveToTable(Bystandersx, Bystandersy, facedown)

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def flip(card, x = 0, y = 0):
    mute()
    if card.isFaceUp == True:
      notify("{} flips {} face down.".format(me, card))
      card.isFaceUp = False
    else:
      card.isFaceUp = True
      notify("{} flips {} face up.".format(me, card))
    
def discard(card, x=0, y=0):
    mute()
    if card.controller != me:
        whisper("{} does not control '{}' - discard cancelled".format(me, card))
        return
    
    pile = card.controller.piles['Discard Pile']
    who = pile.controller
    notify("{} discards '{}'".format(me, card))
    if who != me:
        card.setController(who)        
        remoteCall(who, "doDiscard", [me, card, pile])
    else:
        doDiscard(who, card, pile)
        
def doDiscard(player, card, pile):
    card.moveTo(pile)

def KO(card, x=0, y=0):
    mute()
    if card.controller !=me:
        whisper("{} does not control '{}'".format(me,card))
        return
        
    pile= shared.piles['KO_Pile']
    who = pile.controller
    notify("'{}' is KO'd!".format(card))
    if who != me:
        card.setcontroller(who)
        remoteCall(who, "doKO", [me, card, pile])
    else:
        doKO(who, card, pile)
        
def doKO(player, card, pile):
    card.moveTo(pile)

def defeat(card, x=0, y=0):
    mute()
    if card.controller != me:
        whisper("{} does not control '{}'".format(me,card))
        return
        
    pile = card.controller.piles['Victory Pile']
    who = pile.controller
    notify("{} defeats '{}'!".format(me, card))
    if who != me:
        card.setController(who)
        remoteCall(who, "doDefeat", [me, card, pile])
    else:
        doDefeat(who, card, pile)
        
def doDefeat(player, card, pile):
    card.moveTo(pile)
    
def escape(card, x=0, y=0):
    mute()
    if card.controller != me:
        whisper("{} does not control '{}'".format(me,card))
        return
    
    pile = shared.piles['Escaped_Villains']
    who = pile.controller
    notify("Nooooo! '{}' escaped!".format(card))
    if who != me:
        card.setcontroller(who)
        remoteCall(who, "doEscape", [me, card, pile])
    else:
        doEscape(who, card, pile)
        
def doEscape(player, card, pile):
    card.moveTo(pile)
    
#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------

def randomDiscard(group):
    mute()
    card = group.random()
    if card is None: return
    notify("{} randomly discards '{}'.".format(me, card))
    card.moveTo(me.piles['Discard Pile'])

#------------------------------------------------------------------------------
# Pile Actions
#------------------------------------------------------------------------------

def draw(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group[0]
    card.moveTo(me.hand)
    notify("{} draws '{}'".format(me, card))

def drawMany(group, count = None):
    mute()
    if len(group) == 0: return
    if count is None:
        count = askInteger("Draw how many cards?", 6)
    if count is None or count <= 0:
        whisper("drawMany: invalid card count")
        return
    for c in group.top(count):
        c.moveTo(me.hand)
        notify("{} draws '{}'".format(me, c))

def shuffle(group):
    mute()
    if len(group) > 0:
        update()
        group.shuffle()
        notify("{} shuffles {}".format(me, group.name))
 
def lookAtTop1Deck(group, x = 0, y = 0):
    mute()
    notify("{} looks at {}'s Deck.".format(me, me))
    me.deck.lookAt(1,True)

def lookAtTop3Deck(group, x = 0, y = 0):
    mute()
    notify("{} looks at {}'s Deck.".format(me, me))
    me.deck.lookAt(3,True)

def moveAllToPlayer(group):
    mute()
    if confirm("Shuffle all cards from {} to Player Deck?".format(group.name)):
        for c in group:
            c.moveTo(c.controller.piles['Player Deck'])
        notify("{} moves all cards from {} to the Player Deck".format(me, group.name))
        shuffle(me.piles['Player Deck'])
