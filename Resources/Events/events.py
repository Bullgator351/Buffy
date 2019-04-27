#script version 3.1.0.0 or 3.1.0.1
def counterChangeEvent(player,counter,oldValue):
	notify("{} changes {} counter from {} to {}" .format(player,counter,oldValue,counter.value))
	

	
#script version 3.1.0.2
def counterChangeEvent(args):
	notify("{} changes {} counter from {} to {}" .format(args.player,args.counter,args.oldValue,counter.value))
	