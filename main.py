import random
import time

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11,
}

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit} with a value of {self.value}'

    def ace_adjustment(self):
        if self.rank == 'Ace':
            if self.value == 11:
                self.value = 1
            else:
                self.value = 11

class Deck:
    
    def __init__(self):
        self.cards = [Card(x, y) for x in suits for y in ranks]

    def shuffle(self):
        print('Shuffling cards...')
        random.shuffle(self.cards)
        time.sleep(1)
        print('Cards have been shuffled')

    def deal(self):
        return self.cards.pop()

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def hit(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1
            self.adjust_for_aces()
            card.ace_adjustment()

    def adjust_for_aces(self):
        if self.value > 21:
            self.value -= 10

class Dealer:

    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def display_hand(self):
        print('\n')
        print('DEALER HAND:')
        for card in self.hand.cards[1:]:
            print(card)

class Player(Dealer):

    def __init__(self, name):
        Dealer.__init__(self, name)
        self.chips = 100

    def collect_winnings(self, amount):
        self.chips += amount

class Game:

    def __init__(self):
        self.playing = True
        self.turn = 'P'
        self.pot = 0
        self.deck = None
        self.dealer = Dealer('Morgan')
        self.player = None
        self.winner = False

    def initialize_player(self):
        
        print('Welcome to Python Casinos and Resorts!')
        print('My name is Morgan and I will be your dealer for today!')

        time.sleep(1)

        name = input('May I get your name? ')

        self.player = Player(name)

        time.sleep(1)

        print(f'Thank you, {self.player.name}. I will start you off with {self.player.chips} chips. Let\'s get started!')

    def get_player_move(self):

        print(f'Your current hand has a value of {self.player.hand.value}')
        time.sleep(1)

        while True:
        
            print('\n')
            hit = input('Would you like to hit or stay? ')

            if hit.lower() != 'hit' and hit.lower() != 'stay':
                print('That is not a valid option. Please try again.')
                continue
            else:
                if hit.lower() == 'hit':
                    card = self.deck.deal()

                    self.player.hand.hit(card)

                    print('\n')
                    print(f'{self.player.name}, has been dealt {card.rank} of {card.suit} bringing their total to {self.player.hand.value}.')                    
                    break
                if hit.lower() == 'stay':
                    print('\n')
                    print(f'{self.player.name}, has decided to stay with a hand value of {self.player.hand.value}.')
                    self.turn = 'D'
                    break

    def get_player_bet(self):

        
        print(f'{self.player.name}, you currently have {self.player.chips} chips.')
        time.sleep(.5)

        while True:

            try:
                bet = int(input('How much would you like to bet? '))
            except TypeError:
                print('That is not a valid amount. Please try again.')
                continue
            except bet > self.player.chips:
                print('You do not have enough chips for that wage. Please try again.')
                continue
            else:
                print(f'You have placed a bet of {bet}. Good Luck!')
                # bet_amount * 2 to account for the dealer matching the bet of the player in the pot
                self.player.chips -= bet
                self.pot += bet*2
                break

    def payout(self):
        if self.winner == False:
            self.pot = 0
        else:
            self.player.collect_winnings(self.pot)
            self.pot = 0

    def initial_deal(self):
        for i in range(2):
            self.dealer.hand.hit(self.deck.deal())
            self.player.hand.hit(self.deck.deal())

    def check_hand_for_bust(self, hand):
        if hand.value > 21:
            return True
        else:
            return False  

    def check_play_again(self):

        if self.player.chips == 0:
            print('\n')
            print('I am sorry, you do not have enough chips to play again.')
            return False

        play_again = ''

        while play_again.lower() != 'y' or play_again.lower() != 'n':

            play_again = input('Would you like to play again? (y/n): ')

            if play_again.lower() != 'y' and play_again.lower() != 'n':
                print('That is not a valid choice. Please try again.')
                continue
            else:
                if play_again.lower() == 'y':
                    return True
                else:
                    return False
        
    def reset_hands(self):
        self.dealer.hand = Hand()
        self.player.hand = Hand()
        self.winner = False
        self.turn = 'P'
        
    def play(self):
        ## INITIALIZE THE PLAYER
        self.initialize_player()
                
        ## START GAME

        while self.playing:

            self.deck = Deck()
            self.deck.shuffle()

            ## TAKE THE PLAYERS BET
            self.get_player_bet()

            print('Dealing Cards...')
            time.sleep(2)

            ## DEAL TWO CARDS TO THE DEALER AND THE PLAYER
            self.initial_deal()

            ## DISPLAY BOTH PLAYER CARDS AND DISPLAY ONE DEALER CARD
            self.player.display_hand()
            self.dealer.display_hand()

            time.sleep(2)

            ## WHILE IT IS THE PLAYERS TURN
            while self.turn == 'P':    
                ## ASK IF THEY WOULD LIKE TO HIT OR STAY
                print('\n')
                self.get_player_move()
               
               ## CHECK IF THE PLAYER HAS BUST
                if self.check_hand_for_bust(self.player.hand):
                    print(f'OH NO! {self.player.name} has busted!')
                    print(f'I have won the pot of {self.pot}')
                    self.payout()

                   # ASK TO PLAY AGAIN
                    if self.check_play_again():
                        self.reset_hands()
                        break
                    else:
                        self.playing = False
                        print(f'{self.player.name} has cashed out with {self.player.chips} chips! Have a great day!')
                        break

                elif self.player.hand.value == 21:
                    print(f'{self.player.name} has hit 21!')
                    print(f'{self.player.name} has won the pot of {self.pot}')
                    self.winner = True
                    self.payout()

                    # ASK TO PLAY AGAIN
                    if self.check_play_again():
                        self.reset_hands()
                        break
                    else:
                        self.playing = False
                        print(f'{self.player.name} has cashed out with {self.player.chips} chips! Have a great day!')
                        break

                else: 
                    continue

            ## WHILE IT IS THE DEALERS TURN
            while self.turn == 'D':

                ## DEAL CARDS TO THE DEALERS HAND UNTIL THE DEALERS HAND VALUE IS CLOSER TO 21 THAN THE PLAYER OR THE VALUE EXCEEDS 21
                if self.dealer.hand.value < self.player.hand.value and self.dealer.hand.value < 21:
                    self.dealer.hand.hit(self.deck.deal())
                else:

                    if self.dealer.hand.value > 21:
                        print(f'OH NO! I have busted!')
                        print(f'{self.player.name} has won the pot of {self.pot}')
                        self.winner = True
                        self.payout()

                        # ASK TO PLAY AGAIN
                        if self.check_play_again():
                            self.reset_hands()
                            break
                        else:
                            self.playing = False
                            print(f'{self.player.name} has cashed out with {self.player.chips} chips! Have a great day!')
                            break

                    elif self.dealer.hand == 21:
                        print(f'I have hit 21!')
                        print(f'I have won the pot of {self.pot}')
                        self.payout()

                        # ASK TO PLAY AGAIN
                        if self.check_play_again():
                            self.reset_hands()
                            break
                        else:
                            self.playing = False
                            print(f'{self.player.name} has cashed out with {self.player.chips} chips! Have a great day!')
                            break
                    else:
                        if self.dealer.hand.value <= self.player.hand.value:
                            continue
                        else:
                            print(f'I have won with a score of {self.dealer.hand.value}')
                            print(f'I have won the pot of {self.pot}')
                            self.payout()

                            # ASK TO PLAY AGAIN
                            if self.check_play_again():
                                self.reset_hands()
                                break
                            else:
                                self.playing = False
                                print(f'{self.player.name} has cashed out with {self.player.chips} chips! Have a great day!')
                                break


if __name__ == '__main__':
    Game = Game()

    Game.play()



    




