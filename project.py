import random
import argparse
import time

class Hand:
    def __init__(self):
        self._cards = []
    
    def value(self):
        """Calculates the value of the hand in Blackjack."""
        value = 0
        aces = 0
        for card in self.cards:
            rank, _ = card
            if rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif rank == 'Ace':
                aces += 1
                value += 11  # Initially count Ace as 11
            else:
                value += int(rank)
        
        # Adjust for Aces if value exceeds 21
        while value > 21 and aces:
            value -= 10  # Count one Ace as 1 instead of 11
            aces -= 1
        return value

    def display_value(self):
        """Returns a display-friendly value for the hand, such as 8/18."""
        value = self.value()
        if any(rank == 'Ace' for rank, _ in self.cards) and sum(int(rank) if rank.isdigit() else 10 for rank, _ in self.cards if rank != 'Ace') < 11:
            alternate_value = value - 10
            if alternate_value > 0:
                return f"{alternate_value}/{value}"
        return str(value)
    
    def __str__(self):
        return ', '.join([f"{rank} of {suit}" for rank, suit in self.cards])
    
    @property
    def cards(self):
        return self._cards
    
    @cards.setter
    def cards(self, value):
        self._cards = value
    

def main():
    print("Welcome to Blackjack!") # Welcome message
    deck = createdeck() # Create a deck of cards
    deck = shuffledeck(deck) # Shuffle the deck
    hands = [Hand() for _ in range(args.players + 1)]  # Create Hand objects for each player and the dealer
    hands = dealhands(deck, hands)  # Deal hands to specified number of players and the dealer
    print(f"Dealer's Face Up Card: {hands[0].cards[1][0]} of {hands[0].cards[1][1]}")  # Show the dealer's face-up card
    hit_or_stand(hands, deck)  # Allow players to hit or stand
    hand_values = [hand.value() for hand in hands]  # Calculate hand values for all players and dealer
    print(f"Dealer's Hand: {hands[0]} - Value: {hands[0].display_value()}")
    dealers_turn(hands, deck, hand_values)  # Dealer's turn to hit or stand
    for hand in hands[1:]:
        time.sleep(1)
        print(f"Player {hands.index(hand)}: {result_hand(hand, hands[0])}") #Outputs Result

def createdeck():
    """Creates a deck of cards."""
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return deck

def shuffledeck(deck):
    """Shuffles the deck of cards."""
    random.shuffle(deck)
    return deck

def dealhands(deck, hands):
    """Deals hands to players and dealer into a given set of Hand structures."""
    for i in range(2):  # Deal 2 cards to each player
        for j in range(len(hands)):
            if deck:
                hands[j].cards.append(deck.pop())
            else:
                raise ValueError("Not enough cards in the deck to deal hands.")
    return hands

def hit_or_stand(hands, deck):
    """Prompts the player to hit or stand."""
    for hand in hands[1:]:  # Skip the dealer's hand
        print(f"Player's Hand: {hand} - Value: {hand.display_value()}")
        valid = True
        while valid:
            choice = input("Do you want to hit or stand? (h/s): ")
            if choice.strip().lower() == 'h':
                if deck:
                    hand.cards.append(deck.pop())
                    print(f"New Card: {hand} - New Value: {hand.display_value()}")
                    if hand.value() > 21:
                        print("Bust! You exceeded 21.")
                        valid = False
                else:
                    raise ValueError("Not enough cards in the deck to hit.")
            elif choice.strip().lower() == 's':
                valid = False
            else:
                print("Invalid choice. Please enter 'h' to hit or 's' to stand.")

def dealers_turn(hands, deck, hand_values):
    """Handles the dealer's turn."""
    if min(hand_values[1:]) > 21:
        print("All players have busted. Dealer wins.")
        return
    while hands[0].value() < 17:
        if deck:
            time.sleep(1)  # Allow for slowing of messages
            hands[0].cards.append(deck.pop())
            print(f"Dealer hits: {hands[0]} - New Value: {hands[0].value()}")
        else:
            raise ValueError("Not enough cards in the deck for the dealer to hit.")
    if hands[0].value() > 21:
        time.sleep(1)
        print("Dealer busts! All non busted players win.")

def result_hand(player_hand, dealer_hand):
    """Determines the result of a player's hand against the dealer's hand."""
    player_value = player_hand.value()
    dealer_value = dealer_hand.value()

    if player_value > 21:
        return "Bust! You exceeded 21. Dealer wins."
    elif dealer_value > 21:
        return "Dealer busts! You win."
    elif player_value > dealer_value:
        return "You win!"
    elif player_value < dealer_value:
        return "Dealer wins. You lose."
    else:
        return "It's a tie!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play a game of Blackjack.")
    parser.add_argument("--players", type=int, default=1, help="Number of players (excluding the dealer)")
    args = parser.parse_args()
    main()

def threshold_strategy(hand, threshold=17):
    """Returns 'hit ' if the hand value is below the threshold, otherwise 'stand'."""
    if hand.value() < threshold:
        return 'h'
    else:
        return 's'