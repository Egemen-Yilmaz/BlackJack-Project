#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random


# In[2]:


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}


# In[3]:


playing = True


# In[4]:


class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit


# In[5]:


class Deck:
    
    def __init__(self):
        
        self.deck = [] # Start with an empty list
        
        for suit in suits:
            for rank in ranks:
                #Created All cards
                self.deck.append(Card(suit,rank))
                
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+ card.__str__()
        return "The deck has: "+deck_comp
                
                
    # Shuffle all the deck            
    def shuffle(self):
        random.shuffle(self.deck)
        
    
    def deal(self):
        single_card = self.deck.pop()
        return single_card


# In[6]:


#test_deck = Deck()
#test_deck.shuffle()
#print(test_deck)


# In[7]:


class Hand:
    
    def __init__(self):
        self.cards = []   # start with an empty list as we did in the Deck class
        self.value = 0    # start with zero value
        self.aces = 0     # add an attribute to keep track of aces
        
        
    def add_card(self,card):
        # card passed in
        # from Deck.deal() --> single Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]
        
        # Track aces
        if card.rank == 'Ace':
            self.aces += 1
        
    def adjust_for_ace(self,hand):
        
        
        # IF TOTAL VALUE > 21 AND I STILL HAVE AN ACE
        # THAN CHANGE MY ACE TO BE A 1 INSTEAD OF AN 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# In[8]:


test_deck = Deck()
test_deck.shuffle()

#Player
test_player = Hand()
# Deal 1 card from the deck CARD(suit,rank)
pulled_card = test_deck.deal()
print(pulled_card)
test_player.add_card(pulled_card)
print(test_player.value)


# In[9]:


class Chips:
    
    def __init__(self):
        self.total = 300
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        
    def lose_bet(self):
        self.total -= self.bet


# In[10]:


def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input("Enter your bet: "))
        except:
            print("Looks like you did not enter an integer!")
        else:
            if chips.bet > chips.total:
                print('Sorry, you do not have enough chips!!  You have: {}'.format(chips.total))
            else:
                break
                


# In[11]:


def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace(deck)


# In[12]:


def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break


# In[13]:


def show_some(player,dealer):
    
    # Show only ONE of the dealer's cards
    print("\n Dealer's Hand: ")
    print("First card hidden!!")
    print(dealer.cards[1])
    
    # Show all (2 cards) of the player's hand/cards
    print("\n Player's Hand: ")
    for card in player.cards:
        print(card)
    
    
    
def show_all(player,dealer):
    
    # Show all the dealer's cards
    print("\n Dealer's Hand: ")
    for card in dealer.cards:
        print(card)
        
        
    # Calculate and display value (J+K == 20)
    print("Value of Dealer's hand is : {}".format(dealer.value))
    
    # Show all player's cards
    print("\n Player's Hand: ")
    for card in player.cards:
        print(card)
    
    # Calculate and display value (J+K == 20)
    print("Value of Dealer's hand is : {}".format(player.value))
            


# In[14]:


def player_busts(player,dealer,chips):
    print("BUST PLAYER!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("PLAYER WINS!  DEALER BUST!!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("DEALER WINS!")
    chips.lose_bet()
    
def push(player,dealer):
    print('Dealer and pllayer tie! PUSH')


# In[15]:


while True:
    # Print an opening statement
    print('\n Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
            
    # Set up the Player's chips
    player_chips = Chips()  # remember the default value is 100    
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand) 
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)  
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break        


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)    
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)        
    
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at",player_chips.total)
    
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




