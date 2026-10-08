import pytest
from project import Hand, createdeck, dealhands, dealers_turn, hit_or_stand, result_hand, threshold_strategy, play_hand, simulate_game, simulate_games

def test_create_deck():
    deck = createdeck()
    assert len(deck) == 52
    assert all(isinstance(card, tuple) for card in deck)
    assert all(len(card) == 2 for card in deck)

def test_deal_hands():
    deck = createdeck()
    hands = [Hand() for _ in range(3)]  # 2 players + 1 dealer
    hands = dealhands(deck, hands)
    assert len(hands) == 3  # 2 players + 1 dealer
    for hand in hands:
        assert len(hand.cards) == 2  # Each hand should have 2 cards
    
    deck = createdeck()
    hands = [Hand() for _ in range(27)]  # 26 players + 1 dealer
    with pytest.raises(ValueError):
        dealhands(deck, hands)  # Not enough cards to deal to 26 players + dealer

def test_dealers_turn():
    deck = createdeck()
    hands = [Hand() for _ in range(2)]  # 1 player + 1 dealer
    hands = dealhands(deck, hands)
    hand_values = [hand.value() for hand in hands]
    dealers_turn(hands, deck, hand_values)
    assert hands[0].value() >= 17 or hands[0].value() > 21  # Dealer should hit until at least 17 or bust

    deck = createdeck()
    hands = [Hand() for _ in range(26)]  # 25 player + 1 dealer
    hands = dealhands(deck, hands)
    hand_values = [hand.value() for hand in hands]
    if hand_values[0] < 17:
        with pytest.raises(ValueError):
            dealers_turn(hands, deck, hand_values)

def test_result_hand():
    hand1 = Hand()
    hand1.cards.append(('10', 'Hearts'))
    hand1.cards.append(('7', 'Diamonds'))
    hand2 = Hand()
    hand2.cards.append(('9', 'Clubs'))
    hand2.cards.append(('9', 'Spades'))
    assert result_hand(hand1, hand2) == "Dealer wins. You lose."
    hand3 = Hand()
    hand3.cards.append(('10', 'Clubs'))
    hand3.cards.append(('7', 'Spades'))
    assert result_hand(hand1, hand3) == "It's a tie!"
    hand4 = Hand()
    hand4.cards.append(('10', 'Clubs'))
    hand4.cards.append(('8', 'Spades'))
    assert result_hand(hand1, hand4) == "Dealer wins. You lose."
    hand1.cards.append(('5', 'Diamonds'))  # Now hand1 is bust
    assert result_hand(hand1, hand4) == "Bust! You exceeded 21. Dealer wins."

def test_hand_value():
    hand = Hand()
    hand.cards.append(('10', 'Hearts'))
    hand.cards.append(('7', 'Diamonds'))
    assert hand.value() == 17
    hand.cards.append(('5', 'Clubs'))
    assert hand.value() == 22  # Bust
    hand = Hand()
    hand.cards.append(('Ace', 'Hearts'))
    hand.cards.append(('7', 'Diamonds'))
    assert hand.value() == 18  # Ace counts as 11
    hand.cards.append(('Ace', 'Clubs'))
    assert hand.value() == 19  # Two Aces, one counts as 11, the other as 1
    hand.cards.append(('7', 'Spades'))
    assert hand.value() == 16  # Bust with two Aces and two Sevens
    hand.cards.append(('9', 'Diamonds'))
    assert hand.value() == 25  # Bust with two Aces, two Sevens and a Nine

def test_display_value():
    hand = Hand()
    hand.cards.append(('Ace', 'Hearts'))
    hand.cards.append(('7', 'Diamonds'))
    assert hand.display_value() == "8/18"  # Ace can be 1 or 11
    hand.cards.append(('5', 'Clubs'))
    assert hand.display_value() == "13"  # Ace counts as 11, total is 18
    hand.cards.append(('Ace', 'Spades'))
    assert hand.display_value() == "14"  # Two Aces, one counts as 11, the other as 1

def test_str_representation():
    hand = Hand()
    hand.cards.append(('10', 'Hearts'))
    hand.cards.append(('7', 'Diamonds'))
    assert str(hand) == "10 of Hearts, 7 of Diamonds"
    hand.cards.append(('Ace', 'Clubs'))
    assert str(hand) == "10 of Hearts, 7 of Diamonds, Ace of Clubs"

def test_hit_or_stand(monkeypatch):
    deck = createdeck()
    hands = [Hand() for _ in range(2)]  # 1 player + 1 dealer
    hands = dealhands(deck, hands)
    
    # Simulate player choosing to hit and then stand
    inputs = iter(['h', 's'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    hit_or_stand(hands, deck)
    
    # After hitting, the player's hand should have 3 cards
    assert len(hands[1].cards) == 3

def test_threshold_strategy():
    hand = Hand()
    hand.cards.append(('9', 'Hearts'))
    hand.cards.append(('7', 'Diamonds'))
    
    # Test the threshold strategy
    strategy = threshold_strategy(17)
    assert strategy(hand) == 'h'  # Player should hit if value is below threshold
    strategy = threshold_strategy(15)
    assert strategy(hand) == 's'  # Player should stand if value is above threshold
    strategy = threshold_strategy(16)
    assert strategy(hand) == 's'  # Player should stand if value is at threshold
    
def test_play_hand():
    deck = [('10', 'Spades'), ('2', 'Hearts'), ('4', 'Diamonds'), ('2', 'Clubs')]
    strategy = threshold_strategy(16)
    hand = Hand()
    hand.cards.append(('6', 'Hearts'))
    hand.cards.append(('3', 'Diamonds'))
    play_hand(deck, hand, strategy)
    assert len(hand.cards) == 5  # Player should have until reaching 16 or more hit and have received 3 cards
    hand = Hand()
    hand.cards.append(('10', 'Hearts'))
    hand.cards.append(('7', 'Diamonds'))
    play_hand(deck, hand, strategy)  # Threshold is 16, player should stand
    assert len(hand.cards) == 2  # Player should have 2 cards and not hit
    hand = Hand()
    hand.cards.append(('10', 'Hearts'))
    hand.cards.append(('4', 'Diamonds'))
    play_hand(deck, hand, strategy)  # Threshold is 16, player should hit
    assert len(hand.cards) == 3  # Player should have bust and finish with three cards
    hand = Hand()
    hand.cards.append(('10', 'Hearts'))
    hand.cards.append(('3', 'Diamonds'))
    with pytest.raises(ValueError):
        play_hand(deck, hand, strategy)  # Deck should run out of cards and raise ValueError

def test_simulate_game():
    strategy = threshold_strategy(17)
    result = simulate_game(strategy)
    assert result["result"] in ["win", "lose", "push"]
    assert isinstance(result["player_value"], int)
    assert isinstance(result["dealer_value"], int)
    assert isinstance(result["player_bust"], bool)
    assert isinstance(result["dealer_bust"], bool)
    deck = [('10', 'Spades'), ('2', 'Hearts'), ('4', 'Diamonds'), ('8', 'Clubs'), ('6', 'Hearts'), ('10', 'Diamonds'), ('9', 'Clubs'), ('Queen', 'Spades')]
    result = simulate_game(strategy, deck)
    assert result["result"] == "lose"  # Player should lose with the given deck and strategy
    assert result["player_value"] == 23
    assert result["dealer_value"] == 20
    assert result["player_bust"] is True
    assert result["dealer_bust"] is False
    deck = [('10', 'Spades'), ('2', 'Hearts'), ('7', 'Diamonds'), ('4', 'Clubs'), ('6', 'Hearts'), ('6', 'Diamonds'), ('9', 'Clubs'), ('Queen', 'Spades')]
    result = simulate_game(strategy, deck)
    assert result["result"] == "win"  # Player should win with the given deck and strategy
    assert result["player_value"] == 19
    assert result["dealer_value"] == 23
    assert result["player_bust"] is False
    assert result["dealer_bust"] is True
    deck = [('10', 'Spades'), ('2', 'Hearts'), ('3', 'Diamonds'), ('4', 'Clubs'), ('6', 'Hearts'), ('6', 'Diamonds'), ('9', 'Clubs'), ('Queen', 'Spades')]
    result = simulate_game(strategy, deck)
    assert result["result"] == "push"  # Player should push with the given deck and strategy
    assert result["player_value"] == 19
    assert result["dealer_value"] == 19
    assert result["player_bust"] is False
    assert result["dealer_bust"] is False

def test_simulate_games():
    strategy = threshold_strategy(17)
    results = simulate_games(strategy, num_games=1000)
    assert results["games"] == 1000
    assert (results["wins"] + results["losses"] + results["pushes"]) == 1000
    assert results["win_rate"] == results["wins"] / 1000
    assert results["loss_rate"] == results["losses"] / 1000
    assert results["push_rate"] == results["pushes"] / 1000
    assert results["expected_return"] == (results["wins"] - results["losses"]) / 1000
    assert 0 <= results["win_rate"] <= 1
    assert 0 <= results["loss_rate"] <= 1
    assert 0 <= results["push_rate"] <= 1
    assert abs(results["win_rate"] + results["loss_rate"] + results["push_rate"] - 1) < 1e-10  # Rates should sum to 1
    with pytest.raises(ValueError):
        simulate_games(strategy, num_games=-1)  # Negative number of games should raise ValueError
        simulate_games(strategy, num_games=0)  # Zero games should raise ValueError