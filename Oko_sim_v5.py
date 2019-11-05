import random
from collections import Counter
from itertools import combinations
import sys
import numpy as np
import pandas as pd

#import sys
#sys.stdout = open('outputfile.txt', 'w')

def log(s):
    if DEBUG:
        print(s)

DEBUG = False

decklist = {
	'Forest': 7,
	'Breeding Pool': 4,
	'Hollowed Fountain': 4,
	'Gilded Goose': 4,
	'Arboreal Grazer': 3,
	'Oko, Thief of Crowns': 4,
	'Once Upon a Time': 4,
	'Temple Garden': 4,
	'Temple of Mystery': 2,
	'Island': 4,
	'Castle Vantress': 2,
	'Fabled Passage': 2,
	'Other': 16 
}

if sum(decklist.values()) != 60:
	print('The deck does not contain 60 cards')

#This function is for Once Upon a Time.
def choose_keep(hand, cardsrevealed, keepnumber):
	"""	
	Parameters:
		hand - A dictionary, with the same cardnames as in deck, with number drawn
		number_remaining_discard - 2 for Faithless Looting and 1 for Insolent Neonate
	Returns - a list of the cards to discard, based on a fixed priority order
	"""
	answer = []
	
	#If don't have an untapped green source, keep one of those.
	if (hand['Breeding Pool'] +  hand['Temple Garden'] + hand['Forest'] == 0):
		priority_list = ['Breeding Pool', 'Temple Garden', 'Forest']
	
	#Else, if you don't have a Goose or Grazer, then take a Goose followed by a Grazer.
	elif (hand['Gilded Goose'] == 0 and hand['Arboreal Grazer'] == 0):
		priority_list = ['Gilded Goose', 'Arboreal Grazer']
	
	#Else, if you have a Goose, take a land starting with untapped sources.
	elif (hand['Gilded Goose'] >= 1):
		priority_list = ['Breeding Pool', 'Temple Garden', 'Forest', 'Island', 'Castle Vantress', 'Temple of Mystery', 'Fabled Passage', 'Hollowed Fountain']
	
	#Note that if you have a Grazer, exactly 1 land (untapped green source), no Goose, and a Once Upon, 
	#there is an advantage in taking a Goose over a land. This is because it fixes a blue land for you. If
	#there isn't a blue source revealed, and you take it, there is a chance you'll draw an untapped land
	#on turn-2 that isn't blue. That's why we priortize blue sources. But in both cases (Goose vs. land), 
	#you will have to draw an untapped land.
	#Note also that cards are placed on the bottom, so there is no advantage in taking a tap land over 
	#an untap land in order to have a greater chance of drawing a tap land on turn 2. 
	elif (hand['Arboreal Grazer'] >= 1):
		priority_list = ['Gilded Goose', 'Breeding Pool', 'Island', 'Castle Vantress', 'Temple of Mystery', 'Fabled Passage', 'Hollowed Fountain', 'Temple Garden', 'Forest']
		
	for card in priority_list:
		number_to_keep = min(cardsrevealed[card], keepnumber)
		answer += [card] * number_to_keep
		keepnumber = max(0, keepnumber - number_to_keep)
	
	return answer

def describe_game_state(hand, battlefield, graveyard, library): 
	"""	
	This function is used while debugging simulate_one_game
	"""
	log("")
	log("Hand is now:")
	log(hand)
	log("Battlefield is now:")
	log(battlefield)
	log("Graveyard is now:")
	log(graveyard)
	log("Library is now:")
	log(Counter(library))
	log("")

def play_OnceUponaTime(deck, library, hand, battlefield, graveyard): 
	hand['Once Upon a Time'] -= 1
	graveyard['Once Upon a Time'] += 1
	log('Our hand is: ' + str(hand))
	tempCards = {}
	for card in deck.keys():
		tempCards[card] = 0
	log("We play a Once Upon a Time.\n")
	for _ in range(5):
		card_drawn = library.pop(0)
		tempCards[card_drawn] += 1
		log("We reveal: " + card_drawn +"\n")
	#Use the function choose_keep to figure out which card to keep.
	card_to_keep = choose_keep(hand, tempCards, 1)
	for card in card_to_keep:
		tempCards[card] -= 1
		hand[card] += 1
		log("We keep: " + card +"\n")
	
def play_TempleofMystery(hand, battlefield, graveyard, library): 
	hand['Temple of Mystery'] -= 1
	battlefield['Temple of Mystery'] += 1
	log("We played Temple of Mystery.")
	describe_game_state(hand, battlefield, graveyard, library)

def play_FabledPassage(hand, battlefield, graveyard, library): 
	hand['Fabled Passage'] -= 1
	battlefield['Fabled Passage'] += 1
	log("We played Fabled Passage.")
	describe_game_state(hand, battlefield, graveyard, library)
	
def play_CastleVantress(hand, battlefield, graveyard, library): 
	hand['Castle Vantress'] -= 1
	battlefield['Castle Vantress'] += 1
	log("We played Castle Vantress.")
	describe_game_state(hand, battlefield, graveyard, library)
	
def play_Island(hand, battlefield, graveyard, library): 
	hand['Island'] -= 1
	battlefield['Island'] += 1
	log("We played Island.")
	describe_game_state(hand, battlefield, graveyard, library)
	
def play_HollowedFountain(hand, battlefield, graveyard, library): 
	hand['Hollowed Fountain'] -= 1
	battlefield['Hollowed Fountain'] += 1
	log("We played Hollowed Fountain.")
	describe_game_state(hand, battlefield, graveyard, library)
	
def play_BreedingPool(hand, battlefield, graveyard, library): 
	hand['Breeding Pool'] -= 1
	battlefield['Breeding Pool'] += 1
	log("We played Breeding Pool.")
	describe_game_state(hand, battlefield, graveyard, library)
	
def play_Forest(hand, battlefield, graveyard, library): 
	hand['Forest'] -= 1
	battlefield['Forest'] += 1
	log("We played Forest.")
	describe_game_state(hand, battlefield, graveyard, library)
	
def play_TempleGarden(hand, battlefield, graveyard, library): 
	hand['Temple Garden'] -= 1
	battlefield['Temple Garden'] += 1
	log("We played Temple Garden.")
	describe_game_state(hand, battlefield, graveyard, library)

def play_GildedGoose(hand, battlefield, graveyard, library):
	hand['Gilded Goose'] -= 1
	battlefield['Gilded Goose'] += 1
	log("We played Gilded Goose.")
	describe_game_state(hand, battlefield, graveyard, library)
	
def play_ArborealGrazer(hand, battlefield, graveyard, library):
	hand['Arboreal Grazer'] -= 1
	battlefield['Arboreal Grazer'] += 1
	log("We played Arboreal Grazer")
	if (hand['Temple of Mystery'] >= 1):
		play_TempleofMystery(hand, battlefield, graveyard, library)
	elif (hand['Fabled Passage'] >= 1):
		play_FabledPassage(hand, battlefield, graveyard, library)
	elif (hand['Castle Vantress'] >= 1):
		play_CastleVantress(hand, battlefield, graveyard, library)
	elif (hand['Island'] >= 1):
		play_Island(hand, battlefield, graveyard, library)
	elif (hand['Hollowed Fountain'] >= 1):
		play_HollowedFountain(hand, battlefield, graveyard, library)
	elif (hand['Breeding Pool'] >= 1):
		play_BreedingPool(hand, battlefield, graveyard, library)
	elif (hand['Forest'] >= 1):
		play_Forest(hand, battlefield, graveyard, library)
	elif (hand['Temple Garden'] >= 1):
		play_TempleGarden(hand, battlefield, graveyard, library)
		
def play_Oko(hand, battlefield, graveyard, library):
	hand['Oko, Thief of Crowns'] -= 1
	battlefield['Oko, Thief of Crowns'] += 1	
	log("We played Oko!")

##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
	
def simulate_one_game(hand, library, drawfirst):
	"""	
	Parameters:
		hand - A dictionary, with the same cardnames as in deck, with number drawn
		library - A list of 53 or more cards, most of which will be shuffled 
			(but after mull one or more cards on the bottom may be known)
		drawfirst - A boolean that is True if on the draw and False on the play
	Returns - either True (1) if the goal was achieved and False (0) otherwise
	"""
	
	#Initialize variables
	log("----------Start of a new game----------")
	Oko_cast = False
	turn = 1
	battlefield = {}
	graveyard = {}
	for card in decklist.keys():
		graveyard[card] = 0
		battlefield[card] = 0
	
	#TURN 1 GAMEPLAY SEQUENCE	
	
	#Draw a card if on the draw
	log("Welcome to turn "+ str(turn))
	describe_game_state(hand, battlefield, graveyard, library)
	if (drawfirst):
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
		log("We drew: " + card_drawn +"\n")
		
	#Play OnceUpon if have it. 
	#Note: I wrote the keep_logic based on the starting hand. So I can't play
	#a land first in the game logic (which is how I originally coded it)	
	if (hand['Once Upon a Time'] >= 1):
		play_OnceUponaTime(decklist, library, hand, battlefield, graveyard)
	  
	#Play an untapped green source if possible. If we don't have one there
	#is no point playing another land, since turn-2 Oko isn't possible.
	land_played = False 
	if (hand['Breeding Pool'] > 0):
		play_BreedingPool(hand, battlefield, graveyard, library)
		land_played = True
	elif (hand['Temple Garden'] > 0 and land_played == False):
		play_TempleGarden(hand, battlefield, graveyard, library)
		land_played = True
	elif (hand['Forest'] > 0 and land_played == False):
		play_Forest(hand, battlefield, graveyard, library)
		land_played = True
	
	mana_available = battlefield['Breeding Pool'] + battlefield['Temple Garden'] + battlefield['Forest']	
	
	#Play Gilded Goose if possible.
	if (hand['Gilded Goose'] >= 1 and land_played == True):
		play_GildedGoose(hand, battlefield, graveyard, library)
		mana_available -= 1
	
	#Otherwise, play Arboreal Grazer if possible
	if (hand['Gilded Goose'] == 0 and hand['Arboreal Grazer'] >= 1 and land_played == True):
		play_ArborealGrazer(hand, battlefield, graveyard, library)
		mana_available -= 1 

	mana_available = 0 #Resetting mana before turn 2.
	
	#TURN 2 GAMEPLAY SEQUENCE	
	turn = 2
	
	#Draw a card
	log("Welcome to turn "+ str(turn))
	card_drawn = library.pop(0)
	hand[card_drawn] += 1
	log("We drew: " + card_drawn+"\n")
	
	mana_available = battlefield['Breeding Pool'] + battlefield['Temple Garden'] + battlefield['Forest'] + battlefield['Island'] + battlefield['Castle Vantress'] + battlefield['Temple of Mystery'] + battlefield['Fabled Passage'] + battlefield['Hollowed Fountain'] 
	land_played = False 
	
	#If untapped source, play it.
	if (hand['Breeding Pool'] > 0):
		play_BreedingPool(hand, battlefield, graveyard, library)
		land_played = True
	elif (hand['Island'] > 0 and land_played == False):
		play_Island(hand, battlefield, graveyard, library)
		land_played = True
	elif (hand['Temple Garden'] > 0 and land_played == False):
		play_TempleGarden(hand, battlefield, graveyard, library)
		land_played = True
	elif (hand['Forest'] > 0 and land_played == False):
		play_Forest(hand, battlefield, graveyard, library)
		land_played = True 
		
	mana_available += 1 if land_played == True else 0
	
	#If Oko, and conditions are met, play Oko.
	if (hand['Oko, Thief of Crowns'] >= 1 and ((mana_available >= 2 and battlefield['Gilded Goose'] >= 1) or mana_available >= 3)):
		play_Oko(hand, battlefield, graveyard, library)
		Oko_cast = True
		
	#Return True if we were able to cast Oko.
	if (Oko_cast):
		log("Succes!!!\n")
		return True
	else:
		log("Failure!!!\n")
		return False
	
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
		
def simulate_one_specific_hand(hand, bottom, drawfirst, num_iterations):
	"""	
	Parameters:
		hand - A dictionary, with the same cardnames as in deck, with number drawn
		bottom - A dictionary, with the same cardnames as in deck, with cards that will be put on the bottom
			(This is due to London mull. Bottom order is currently arbitrary and assumed to be irrelevant.)
		drawfirst - A boolean that is True if on the draw and False on the play
		num_iterations - Simulation sample size. Could be 10 if precision isn't important, could be 100,000 if it's important.
	Returns - the probability of achieving the goal with this opening hand
	"""
	count_good_hands = 0.0
	
	for i in range(num_iterations):
		
		log("Welcome to iteration number "+ str(i))
		#Copy opening hand information into a variable that can be manipulated in the simulation
		sim_hand = {}
		for card in decklist.keys():
			sim_hand[card] = hand[card]
		
		#Construct the library: first the random part, which gets shuffled
		sim_library = []
		for card in decklist.keys():
			sim_library += [card] * ( decklist[card] - sim_hand[card] - bottom[card])
		random.shuffle(sim_library)
		
		#Then put the bottom part on the bottom
		#The order is assumed not to matter here
		for card in bottom.keys():
			sim_library += [card] * bottom[card]
			
		#Simulate the actual game	
		if simulate_one_game(sim_hand, sim_library, drawfirst)== True:
			count_good_hands += 1
		
	return count_good_hands/num_iterations


def what_to_put_on_bottom (hand, drawfirst, number_bottom, num_iterations):
	"""	
	Parameters:
		hand - A dictionary, with the same cardnames as in deck, with number drawn
		drawfirst - A boolean that is True if on the draw and False on the play
		number_bottom - The number of cards that needs to be put on the bottom
		num_iterations - Simulation sample size. Could be 10 if precision isn't important, could be 10,000 if it's important.
	Returns - A dictionary, with the same cardnames as in deck, with the best set of cards to put on the bottom
	"""	
	best_goal = 0
	best_bottom = {}
	
	#Transform hand into a list to be able to iterate handily
	hand_list = []
	for card in hand.keys():
		hand_list += [card] * hand[card]
	
	#Iterate over all tuples of length number_bottom containing elements from hand_list 
	#There may be duplicates right now, that's bad for runtime but shouldn't affect the maximum
	for bottom in combinations(hand_list, number_bottom):
		log("Currently considering the following bottom:")
		log(bottom)
		#Transform back to dictionary for convenience
		bottom_dict = {}
		for card in decklist.keys():
			bottom_dict[card] = 0
		for card in bottom:
			bottom_dict[card] += 1
		
		remaining_hand = {}
		for card in decklist.keys():
			remaining_hand[card] = hand[card] - bottom_dict[card]
		log("Remaining hand:")
		log(remaining_hand)
		
		goal = simulate_one_specific_hand(remaining_hand, bottom_dict, drawfirst, num_iterations)
		log("Goal: "+str(goal))
		
		if (goal >= best_goal):
			best_goal = goal
			for card in decklist.keys():
				best_bottom[card] = bottom_dict[card]
			log("We now set best_goal to "+str(best_goal)+" and best_bottom to:")
			log(best_bottom)
	
	log("THE BEST BOTTOM IS:")
	log(best_bottom)
	
	return best_bottom
	
def simulate_one_handsize(handsize, drawfirst):
	"""	
	Parameters:
		handsize - Opening hand size, could be in {0, 1, ..., 6, 7}
		drawfirst - A boolean that is True if on the draw and False on the play
	Returns - the probability of achieving the goal with this opening hand size and play/draw setting
	Note - for handsize > 1 the value of success_probability(handsize - 1) needs to be known!!!
	"""
	
	#The following numbers can be adjusted manually to increase/decrease total runtime
	sample_size_for_num_hands = 1000 * handsize if handsize < 7 else 1000 * handsize
	sample_size_per_bottom = 3 * handsize
	sample_size_per_hand_under_best_bottom = 10 * handsize
	
	count_probability = 0.0

	#Construct library as a list
	library = []
	for card in decklist.keys():
		library += [card] * decklist[card]
	log(library)
	
	for iterator in range(sample_size_for_num_hands):
		
		if( iterator > 100 and iterator % 500 == 0):
			print(f'We are now on hand number {iterator}. Current prob = {count_probability / iterator * 100 :.2f} %.')
		log("")
		log("------------Welcome to a new iteration!------------")
		
		#Construct a random opening hand
		#Here, random.sample takes a random sample of 7 cards from library without replacement
		#Feeding that sample into "Counter" gives a dictionary with the number drawn for each cardtype
		opening_hand = Counter(random.sample(library, 7))
		log("")
		log("The opening hand is:" + str(opening_hand))
	
		#Determine the set of cards that are best to put on the bottom
		if (handsize < 7):
			best_bottom = what_to_put_on_bottom(opening_hand, drawfirst, 7 - handsize, sample_size_per_bottom)
		else:
			best_bottom = {} 
			for card in decklist.keys():
				best_bottom[card] = 0
		log("The best bottom is:" + str(best_bottom))
		
		#Take the bottom part from the hand part
		for card in opening_hand.keys():
			opening_hand[card] = opening_hand[card] - best_bottom[card]
		
		#For a 3-card opening hand we auto-keep, since Oko isn't possible with less.
		if (handsize <= 3):
			succes_prob = simulate_one_specific_hand(opening_hand, best_bottom, drawfirst, sample_size_per_hand_under_best_bottom)
			
		#For a larger opening hand we choose keep or mull based on success probability
		if (handsize > 3):
			succes_prob_when_keep = simulate_one_specific_hand(opening_hand, best_bottom, drawfirst, sample_size_per_hand_under_best_bottom)
			succes_prob_when_mull = success_probability[handsize - 1 - 3]
			succes_prob = max(succes_prob_when_keep, succes_prob_when_mull)
			log("Success prob: "+ str(succes_prob))
		count_probability += succes_prob
		
		log("Succes_prob = "+ str(succes_prob))
		
	return count_probability / sample_size_for_num_hands

##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
	
final_prob_for_7 = 0
success_probability = []
for drawfirst in [True, False]:
	#success_probability = [None] * 
	for handsize in range(3,8):
		success_probability.append(simulate_one_handsize(handsize, drawfirst))
		print(f'Drawfirst: {drawfirst}, Handsize: {handsize} = { success_probability[-1] * 100 :.2f}%.') 
		if (handsize == 7):
			final_prob_for_7 += success_probability[-1]
print(f'The final probabilty averaging across the draw and play is {final_prob_for_7 * 50:.2f}%.')

results_df = pd.DataFrame(np.array(success_probability).reshape(2,-1), 
                              columns = ('Hand: 3', 'Hand: 4', 'Hand: 5', 'Hand: 6', 'Hand: 7'))
results_df.rename(index = {0: 'DrawFirst: True', 1: 'DrawFirst: False'}, inplace = True) 
results_df.to_csv("results_df_v2.txt", sep="\t", index=True) 

sys.stdout = open('Simulation_output_v2.txt', 'w')
sample_size_for_num_hands = 1000
sample_size_per_bottom = 3
sample_size_per_hand_under_best_bottom = 10
print('Number of hands to sample for each handsize: ' + str(sample_size_for_num_hands))
print('Number of iterations for each bottom combination: ' + str(sample_size_per_bottom))
print('Number of iterations for the best bottom combination: ' + str(sample_size_per_hand_under_best_bottom))
print('Average 7-handsize probability: ' + str(final_prob_for_7 * .50))
print('Success probabilities: ' + str(success_probability))