import pytest
from project import Hand, createdeck, dealhands, dealers_turn, hit_or_stand, result_hand

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