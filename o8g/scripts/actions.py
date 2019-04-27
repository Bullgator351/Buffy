
DarkLightToken = ("DarkLightToken", "252af8c6-f383-46f9-ae8b-f2f302bdf6b0")
CourageToken = ("CourageToken", "c5be15ab-f1a6-442c-aba1-c64ccc14961b")

# Add global debug
#
# Need to define x and y coordinates of the upper left corner of every pile on the table
# Like bigbadx = this and bigbady = that
# Library and Sunnydale will need to adapt code from LotR that auto spaces the cards out

# Probably table card action but need to compare with flipcard

def flip(card, x = 0, y = 0):
    mute()
    if card.isFaceUp == True:
      notify("{} flips {} face down.".format(me, card))
      card.isFaceUp = False
    else:
      card.isFaceUp = True
      notify("{} flips {} face up.".format(me, card))

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def createDarkLightToken(group, x=0, y=0):
 	moveDarkLightToken(x, y)

def moveCard(model, x, y):
	for c in table:
		if c.model == model:
			c.moveToTable(x, y)
			return c
	return table.create(model, x, y)
	
def moveDarkLightToken(x=0, y=0):
	return moveCard("252af8c6-f383-46f9-ae8b-f2f302bdf6b0", x, y)
	
def getDarkLightToken():
	for c in table:
		if c.model == "252af8c6-f383-46f9-ae8b-f2f302bdf6b0":
			return c
	return None

def getCourageToken():
	for c in table:
		if c.model == "c5be15ab-f1a6-442c-aba1-c64ccc14961b":
			return c
	return None


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
	

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def flipcard(card, x = 0, y = 0):
	mute()
	
	if card.controller != me:
		notify("{} gets {} to flip card".format(me, card.controller()))
		remoteCall(card.controller, "flipcard", card)
		return

	cardx, cardy = card.position
	
# Need playersetup, addencounter or createcard, addresource, discard, something adapted to KO

	
#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------

def randomDiscard(group):
	mute()
	card = group.random()
	if card is None: return
	notify("{} randomly discards '{}'.".format(me, card))
	card.moveTo(me.piles['Discard Pile'])
	
# Need discard and something adapted for KO

#------------------------------------------------------------------------------
# Pile Actions
#------------------------------------------------------------------------------

def shuffle(group):
	mute()
	if len(group) > 0:
		update()
		group.shuffle()
		notify("{} shuffles {}".format(me, group.name))
		
# Need something to track victory conditions - ideally put the number in the global hand display
# Also tract Dark/Light in hand display
