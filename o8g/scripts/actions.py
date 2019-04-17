
DarkLightToken = ("DarkLightToken", "252af8c6-f383-46f9-ae8b-f2f302bdf6b0")
CourageToken = ("CourageToken", "c5be15ab-f1a6-442c-aba1-c64ccc14961b")


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

def shuffle(group):
	mute()
	if len(group) > 0:
		update()
		group.shuffle()
		notify("{} shuffles {}".format(me, group.name))
