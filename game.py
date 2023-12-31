from card import Card
from deck import Deck
from player import Player
from dealer import Dealer

# method to print player and dealer hands


def print_hands():

    print("\nDealer's Hand:")

    if player.is_playing:
        print(f"\t{dealer.hand[0]}")
        print("\tCARD HIDDEN")
    else:
        for card in dealer.hand:
            print(f"\t{card}")

    print("\nPlayer's Hand:")
    for card in player.hand:
        print(f"\t{card}")


def has_ace(user):
    # check if there are any aces worth 11 points in player's hand. If there is, change its value from 11 to 1
    for card in user.hand:
        if card.value == 11:
            user.hand_value -= 10
            card.value = 1  # modify the card's value to ensure the if statement doesn't run for the same card again
            return True
    return False

# announces that there is a blackjack if the user gets a hand of 21


def check_for_blackjack(user):
    if user.hand_value == 21:
        print("\nBLACKJACK!")

# announces that there is a bust if the user's hand exceeds 21


def check_for_bust(user):
    if user.hand_value > 21:
        # if the player has an ace worth 11 points, it will be converted to 1 point and the game will continue
        if not has_ace(user):
            print("\nBUST!")

# First, create a deck of 52 cards


deck = Deck()

# initialize player and dealer objects

player = Player()
dealer = Dealer()

play_game = True  # game will play

# run code here
while play_game:

    # Shuffle the deck

    deck.shuffle()

    print("\nWelcome to Blackjack! The goal is to get as close to 21 as possible without going over!")
    print("The dealer will hit until they reach 17. Aces can count as 1 or 11.\n")

    # Ask the player for their bet

    print(f"You currently have {player.chips} chips.")

    # loop will run until they enter a number that doesn't exceed their number of chips
    while True:
        try:
            bet = int(input("Place your bet: "))
        except:
            print("Please enter a valid number.")
        else:
            # Make sure bet doesn't exceed their chips
            if bet > player.chips:
                print("You have an insufficient number of chips. Please try again.")
            elif bet < 1:
                print("Your must bet at least 1 chip. Please try again.")
            else:
                player.place_bet(bet)
                break

    # deal two cards to player and dealer

    for _ in range(2):
        player.hand.append(deck.deal())
        dealer.hand.append(deck.deal())

    # determine hand value of the player and dealer

    player.hand_value = player.update_hand_value()
    dealer.hand_value = dealer.update_hand_value()

    # show only one of dealers cards; other is hidden
    # show both of player's cards
    print_hands()

    # check for blackjack

    check_for_blackjack(player)

    # ask the player to hit and take another card
    # if they don't bust (go over 21) ask again
    while player.hand_value < 21 and player.is_playing:

        ans = ""

        # ask user to hit or stand until they enter valid input
        while ans.upper() not in ["H", "S"]:
            ans = input("Would you like to hit or stand? ('H' or 'S'): ")

            if ans.upper() not in ["H", "S"]:
                print("Invalid Input. Please try again.")

        # if player hits, deal them a card and update their hand value
        if ans.upper() == "H":
            player.hand.append(deck.deal())

            player.hand_value = player.update_hand_value()
            print_hands()

            # if player gets a blackjack (21 points), claim winnings (doubled to account for original bet)
            check_for_blackjack(player)

            # check if hand is greater than 21
            check_for_bust(player)

        # break out if they choose to stand
        if ans.upper() == "S":
            player.is_playing = False

    # if player stands, play dealer's hand. Dealer will always hit until their value is >= 17. Skip this if the player busted

    if ans.upper() == "S" and player.hand_value <= 21:

        print("Player stands. Dealer is playing...")

        print_hands()

        check_for_blackjack(dealer)

        # dealer will hit until their hand is 17 or greater
        while (dealer.hand_value < 17):
            dealer.hand.append(deck.deal())  # deal the dealer a card

            dealer.hand_value = dealer.update_hand_value()
            print_hands()

            check_for_blackjack(dealer)

            check_for_bust(dealer)

    # determine winner and adjust chips accordingly

    print(f"\nDealer: {dealer.hand_value}")
    print(f"Player: {player.hand_value}")

    # player wins if they have a greater hand and they didn't bust, or if the dealer busts
    if (player.hand_value > dealer.hand_value and player.hand_value <= 21) or dealer.hand_value > 21:
        print("Player wins!")
        # amount is doubled to account for original amount bet
        player.claim_winnings(bet * 2)
    # dealer wins if player has a worse hand or if the player busted
    elif player.hand_value < dealer.hand_value or player.hand_value > 21:
        print("Dealer wins!")
    else:
        print("It's a draw!")
        # if there's a draw, return the player's bet
        player.claim_winnings(bet)

    print(f"\nYou now have {player.chips} chips.")

    # ask player to play again if they have enough chips

    if player.chips > 0:

        while ans.upper() not in ["Y", "N"]:
            ans = input("Would you like to play again? ('Y' or 'N'): ")

            if ans.upper() not in ["Y", "N"]:
                print("Invalid input. Please try again.")

        # exit the game if they choose no
        if ans.upper() == "N":
            play_game = False

        # if they choose to replay, we need to reinitialize everything except for the player's chips
        if ans.upper() == "Y":
            chips = player.chips

            deck = Deck()
            player = Player(chips)
            dealer = Dealer()
    else:
        play_game = False  # exit game if user runs out of chips

print("\nThanks for playing!")

'''
TODOS

loop doesn't ask user to hit or stand again. It continues until they bust
are there any ways to clean up my code?

can I make a method to hit/stand?

'''
