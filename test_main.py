import unittest

from main import Hand, Card, Deck, Player, Game

class TestCard(unittest.TestCase):

    def test_correct_attributes(self):
        '''
        Tests that the attributes on the Card object are assigned correctly.
        '''

        card = Card('Hearts', 'Two')
        self.assertEqual(card.value, 2)
        self.assertEqual(card.suit, 'Hearts')
        self.assertEqual(card.rank, 'Two')
        
    def test_ace_adjustment(self):
        '''
        Ace adjustment method should convert the value of an ace to 1 if it is currently an 11 and vice versa.
        '''
        card = Card('Spades', 'Ace')
        self.assertEqual(card.value, 11)
        card.ace_adjustment()
        self.assertEqual(card.value, 1)
        card.ace_adjustment()
        self.assertEqual(card.value, 11)

class TestDeck(unittest.TestCase):

        def test_creates_complete_deck(self):
            '''
            When a new deck is created, this containing list of cards should contain 52 card objects.
            '''

            deck = Deck()

            self.assertEqual(len(deck.cards), 52)

        def test_shuffles_cards(self):
            '''
            The deck should be in a random order. Meaning the first card should not be two of hearts and the last card should not be the ace of clubs.
            As this is the order they are added in when the deck is created.
            '''

            deck = Deck()
            deck.shuffle()
            two_hearts = Card('Hearts', 'Two')
            ace_clubs = Card('Clubs', 'Ace')


            self.assertNotEqual(deck.cards[0], two_hearts)
            self.assertNotEqual(deck.cards[-1], ace_clubs)

        def test_deals_one(self):
            '''
            This tests that the deal method will remove a single card from the deck.
            '''
            deck = Deck()

            deck.deal()

            self.assertEqual(len(deck.cards), 51)

class TestHand(unittest.TestCase):

    def test_hit_with_jack(self):
        '''
        The hit function should add a card to the list of cards in the hand and update the hands value according to that card's value
        '''

        hand = Hand()
        jack = Card('Hearts', 'Jack')

        hand.hit(jack)

        self.assertEqual(hand.cards, [jack])
        self.assertEqual(hand.value, 10)

    def test_adjusts_ace_when_bust(self):
        '''
        If the hand is dealt an ace, forcing the value of the hand above 21, the value of the ace should be adjusted to 1 to avoid a bust.
        '''
        hand = Hand()

        # Bring initial score within 11 of busting
        five = Card('Hearts', 'Five')
        king = Card('Hearts', 'King')

        hand.hit(five)
        hand.hit(king)

        # Add an ace to force a bust which should trigger ace_adjustment making total value 16
        ace = Card('Hearts', 'Ace')

        hand.hit(ace)

        self.assertEqual(hand.value, 16)

    def test_leaves_aces_without_bust(self):
        '''
        When a hand is dealt an ace, and the value of the hand does not exceed 21, the value of the ace is left at 11.
        '''
        hand = Hand()

        # Bring initial score outside of 11 from busting
        two = Card('Hearts', 'Two')
        three = Card('Hearts', 'Three')

        hand.hit(two)
        hand.hit(three)

        # Add an ace to the hand. Since hand does not bust ace should be added as 11
        # and bring the total value of the hand up to 16
        ace = Card('Clubs', 'Ace')

        hand.hit(ace)

        self.assertEqual(hand.value, 16)
        
class TestPlayer(unittest.TestCase):
    
    def test_collect_winnings(self):
        '''
        When collect winnings is called, the amount passed into the function should be added to the player's chip balance.
        '''

        player = Player('player')

        player.collect_winnings(200)

        self.assertEqual(player.chips, 300)

class TestGame(unittest.TestCase):
    
    def test_check_busted_hand(self):
        '''
        When a hand with a value > 21 is passed to the function it should return True
        '''

        game = Game()
        hand = Hand()

        two = Card('Hearts', 'Two')
        ten = Card('Hearts', 'Ten')
        queen = Card('Hearts', 'Queen')

        hand.hit(two)
        hand.hit(ten)
        hand.hit(queen)

        is_busted = game.check_hand_for_bust(hand)

        self.assertEqual(is_busted, True)

    def test_good_hand(self):
        '''
        When a hand who's value has not exceeded 21 is passed to the function it should return False
        '''

        game = Game()

        hand = Hand()

        ten = Card('Hearts', 'Ten')
        two = Card('Hearts', 'Two')

        hand.hit(ten)
        hand.hit(two)

        is_busted = game.check_hand_for_bust(hand)

        self.assertEqual(is_busted, False)

    def test_play_again_reset(self):
        '''
        reset_hands method should reset the game to a state that another hand can be played from successfully
        '''
        game = Game()

        # Give attributes values that are to be reset
        game.player = Player('Test')
        game.player.hand.hit(Card('Hearts', 'Two'))
        game.player.hand.hit(Card('Clubs', 'King'))
        game.dealer.hand.hit(Card('Clubs', 'Queen'))
        game.dealer.hand.hit(Card('Spades', 'Ace'))
        game.winner = True
        game.turn = 'D'

        # Call the reset function
        game.reset_hands()

        # The above declared variables should be reset to their default values
        # game.dealer.hand = default_hand
        # game.player.hand = default_hand
        # game.winner = False
        # game.turn = 'P'

        self.assertEqual(game.dealer.hand.cards, [])
        self.assertEqual(game.dealer.hand.value, 0)
        self.assertEqual(game.player.hand.cards, [])
        self.assertEqual(game.player.hand.value, 0)
        self.assertEqual(game.winner, False)
        self.assertEqual(game.turn, 'P')

    def test_payout_to_dealer(self):
        '''
        When dealer wins, should simulate a payout to the dealer. Leaving the pot empty.
        '''
        game = Game()

        # Make sure winner variable is set to False, meaning the player did not win
        game.winner = False

        # Add some chips to the pot to simulate a winning
        game.pot += 200

        # Call the payout function
        game.payout()

        self.assertEqual(game.pot, 0)

    def test_payout_to_player(self):
        '''
        When a player wins, they get the balance of the pot added to their chips balance and the game pot is set to zero.
        '''

        # INITIALIZE SCENARIO
        game = Game()
        game.player = Player('Test')
        
        # SIMULATES A BET OF 50 CHIPS
        game.pot += 50*2
        game.player.chips -= 50

        # SET WINNER VARIABLE TO TRUE, MEANING THE PLAYER HAS WON
        game.winner = True

        # CALL PAYOUT FUNCTION
        game.payout()

        # Player begins with a balance of 100, bet 50, and should win double their bet bringing final balance to 150
        self.assertEqual(game.player.chips, 150)
        # Game pot should be depleted
        self.assertEqual(game.pot, 0)


if __name__ == '__main__':
    unittest.main()