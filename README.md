# BLACKJACK PROJECT
#### Video Demo:  https://youtu.be/4LGUGBaFIeY
#### Description:
This project creates a blackjack casino game, that deals hands to a given amount of players, which compete against a dealer controlled by the code. The program is initialised by calling the program name, with an optional --players input after, which can be used to change the amount of players (excluding the dealer) that are dealt in (default value is 1).
Firstly, a standard deck of cards is generated (52), which contain Ace-King of each suit, using createdeck(). The deck is the shuffled, using the random library, and then dealt to the given amount of players and the dealer. In the instance that there are more cards required to be dealt than there are in the deck, a Value Error is raised, as is consistent across the project. After informing the players of the dealers 'face up card', each player is in turn told their cards, and the value of their hand (including hard/soft aces), and then asked whether they want to hit or stand, until they stand or they bust. If the player busts (over 21) they are informed, and their turn ends. Once all players have completed their turns, the dealer also undertakes the process, with the decisions made for them (hit on 16, stand on 17). Each hand is then in turn compared to the dealers, and each player is informed if they won, lost or tied.

### Structures
#### Hand
Hand holds a set of given cards, having been initialised to be empty, and added to using hand.cards as a getter/setter. The functions of Hand are:

**cards()** (getter/setter), which allow for the cards in the hand to either be appended to, or seen

**value()** which outputs the value of the hand, counting aces as 11, unless that will cause the hand to bust, in which case it will be a 1, and any picture cards to be a 10

**display_value()** which outputs not just the value of the cards, but if there is an ace counting as an 11 present, also the alternate value the hand could be when the ace counts as 1 instead

**str()** which outputs the hand as a string "n of suit, n of suit..."

### Functions
#### createdeck()
This function creates a standard deck of 52 cards
#### shuffledeck(deck)
This function shuffles the input deck
#### dealhands(deck, hands)
This function deals hands to to the given number of players plus the dealer from the top of the given deck. hands is the set of Hand structures that will be dealt into, which has been initialised in the main function to be the size of all players plus the dealer. When each card is added to a hand, it is removed from the deck. If a hand is attempted to be dealt to, and there are no cards left in the deck, a Value Error will be raised
#### hit_or_stand(hands, deck)
This function allows each player to undertake their turn. It outputs the players current hand value (including if the value is 'soft'), and prompts the player to either hit or stand (h/s). If "h" entered, a card is dealt from the top of the deck and added to the players hand, and if they have not busted, they will be prompted again. If they have busted, they will be informed, and their turn will end. If the playe instead enters "s", their turn will end. Finally, if the player enters anything other than a case-insensitive, space insensitive "h" or "s", they will be reprompted, with an error message of their invalid choice.
#### dealers_turn(hands, deck, hand_values)
This function undertakes the dealers turn, with inputs of everyone's hands (including the dealers originally first two dealt cards), the remaining deck and the hand values of all other players. If all players have busted, it accepts the victory, and the dealer does not deal any cards. Else, if the dealers hand is worth less than 17, they must hit. If worth 17 (both hard or soft) or more, the dealer must stand. If the dealer attempts to hit, and there are no cards in the deck, a Value Error is raised.

#### result_hand(player_hand, dealer_hand)
This function decides what phrase to output, depending on whether the player or dealer wins (or if there is a tie) and the manner in which they win it (bust or not).
