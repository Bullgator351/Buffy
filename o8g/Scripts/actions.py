def rolldice(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided die.".format(me, n))

def flipcoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
      notify("{} flips heads.".format(me))
    else:
      notify("{} flips tails.".format(me))
	  
def tap(card, x = 0, y = 0):
  mute()
  card.orientation ^= Rot90
  if card.orientation & Rot90 == Rot90:
    notify('{} turns {} sideways'.format(me, card))
  else:
    notify('{} turns {} upright'.format(me, card))

def flip(card, x = 0, y = 0):
    mute()
    if card.isFaceUp == True:
      notify("{} flips {} face down.".format(me, card))
      card.isFaceUp = False
    else:
      card.isFaceUp = True
      notify("{} flips {} face up.".format(me, card))

def discard(card, x = 0, y = 0):
  mute()
  card.moveTo(me.Lost)
  notify("{} discards {} to the lost pile.".format(me, card))

def recirculate(group):
	if len(me.Used) == 0: return
	mute()
	for c in me.Used:
		c.moveToBottom(me.Reserve)
	notify("{} moves the Used pile to the bottom of the Reserve Deck.".format(me))
  
def highlightcard(card, x = 0, y = 0):
  mute()
  if card.highlight == "#ff0000":
    card.highlight = None
    notify('{} removes highlight from {}'.format(me, card))
  else:
    card.highlight = "#ff0000"
    notify('{} highlights {}'.format(me, card))

def activateoldForce(group, x = 0, y = 0):
	if len(me.Reserve) == 0: return
	mute()
	me.Reserve[0] .moveTo(me.Force)
	notify("{} activates 1 force.".format(me))
    
def drawDestiny(group, x = 0, y = 0):
	if len(me.Reserve) == 0: return
	mute()
	me.Reserve[0].moveToTable(400,200,True)
	notify ("{} draws Destiny.".format(me))
		
def draw(group, x = 0, y = 0):
    if len(me.Force) == 0: return
    mute()
    me.Force[0].moveTo(me.hand)
    notify("{} draws a card into hand.".format(me))

def drawOpeningHand(group, x = 0, y = 0, count=None):
    if len(me.Reserve) == 0: return
    mute()
    if count == None: count = askInteger("Deal how many cards to your hand?", 8)
    for c in me.Reserve.top(count): 
        c.moveTo(me.hand)
    notify("{} draws opening hand.".format(me))
	
def useForce(group, x = 0, y = 0):
	if len(me.Force) == 0: return
	mute()
	me.Force[0].moveTo(me.Used)
	notify("{} uses 1 Force.".format(me))
	
def mulligan(group):
	mute()
	if not confirm("Are you sure you want to Mulligan?"): return
	for c in group:
		c.moveToBottom(c.owner.piles['Reserve'])
	notify("{} takes a Mulligan.".format(me))
	me.Reserve.shuffle()
	  
def activateForce(group, x = 0, y = 0, count=None):
    if len(me.Reserve) == 0: return
    mute()
    if count == None: count = askInteger("Activate how many force?", 1)
    for c in me.Reserve.top(count): 
        c.moveTo(me.Force)
    notify("{} activates {} force.".format(me,count))

def dealManyToTableDown(group,count=None):
    dealerid = int(getGlobalVariable("dealer"))
    if me._id != dealerid:
        whisper("You are not the dealer player.")
        return
    if len(shared.Deck) == 0: return
    mute()
    if count == None: count = askInteger("Deal how many cards to table face down?", 5)
    for c in shared.Deck.top(count): 
        c.moveTo(table)
        c.isFaceUp = false
    notify("Dealing {} cards to table face down.".format(count))

def drawManyDown(group, count = None):
    if len(shared.Deck) == 0: return
    mute()
    if count == None: count = askInteger("Draw how many cards?", 7)
    for c in shared.Deck.top(count):
        c.moveTo(me.hand)
        c.isFaceUp = False
    notify("{} draws {} cards face down.".format(me, count))

def mill(group, count = None):
    if len(shared.Deck) == 0: return
    mute()
    if count == None: count = askInteger("Mill how many cards?", 1)
    for c in shared.Deck.top(count): c.moveTo(me.Discard)
    notify("{} mills the top {} cards from the Deck.".format(me, count))

def shuffle(group, x = 0, y = 0):
   mute()
   me.Reserve.shuffle()
   notify("{} shuffled their Reserve Deck.".format(me))
  
def shuffleIntoDeck(group, x = 0, y = 0):
    mute()
    for c in group: c.moveTo(shared.Deck)
    shared.Deck.shuffle()
    notify("{} shuffled the discard pile into the deck.".format(me))

StandardMarker = ("Marker", "40bba10f-82e5-4f7e-986b-e9c850524f88")

def addanymarker(cards, x = 0, y = 0):
    mute()
    marker, quantity = askMarker()
    if quantity == 0: return
    for card in cards:
      card.markers[marker] += quantity
      notify("{} adds {} {} counters to {}.".format(me, quantity, marker[0], card))

def addmarker(card, x = 0, y = 0):
    mute()
    card.markers[StandardMarker] += 1
    notify("{} adds a marker to {}.".format(me, card))

def removemarker(card, x = 0, y = 0):
    mute()
    card.markers[StandardMarker] -= 1
    notify("{} removes a marker from {}.".format(me, card))
