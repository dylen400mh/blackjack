from card import Card
from deck import Deck
from player import Player
from dealer import Dealer

# method to print player and dealer hands


def print_hands(player_hitting=True):

    print("Dealer's Hand:")

    if player_hitting:
        print(dealer.hand[0])
        print("CARD HIDDEN")
    else:
        for card in dealer.hand:
            print(card)

    print("Player's Hand:")
    for card in player.hand:
        print(card)


def has_ace(user):
    # check if there are any aces worth 11 points in player's hand. If there is, change its value from 11 to 1
    for card in user.hand:
        if card.value == 11:
            user.hand_value -= 10
            card.value = 1  # modify the card's value to ensure the if statement doesn't run for the same card again
            return True
    return False


def check_for_blackjack(user):
    if user.hand_value == 21:
        print("BLACKJACK!")


def check_for_bust(user):
    if user.hand_value > 21:

        # if the player has an ace worth 11 points, it will be converted to 1 point and the game will continue
        if not has_ace(user):
            print("BUST!")


# run code here
if __name__ == "__main__":

    # First, create a deck of 52 cards

    deck = Deck()

    # Shuffle the deck

    deck.shuffle()

    # initialize player and dealer objects

    player = Player()
    dealer = Dealer()

    print("Welcome to Blackjack! The goal is to get as close to 21 as possible without going over!")
    print("The dealer will hit until they reach 17. Aces can count as 1 or 11.\n")

    # Ask the player for their bet

    print(f"You currently have {player.chips} chips.")

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

    player_hand_value = player.update_hand_value()
    dealer_hand_value = dealer.update_hand_value()

    # we will use this boolean to determine whether the dealer's card should be hidden or shown
    player_hitting = True

    # show only one of dealers cards; other is hidden
    # show both of player's cards
    print_hands()

    # check for blackjack

    check_for_blackjack(player)

    # ask the player to hit and take another card
    # if they don't bust (go over 21) ask again
    while player_hand_value < 21 and player_hitting:
        ans = ""

        while ans.upper() not in ["H", "S"]:
            ans = input("Would you like to hit or stand? ('H' or 'S'): ")

            if ans.upper() not in ["H", "S"]:
                print("Invalid Input. Please try again.")

        # if player hits, deal them a card and update their hand value
        if ans.upper() == "H":
            player.hand.append(deck.deal())

            player_hand_value = player.update_hand_value()
            print_hands()

            # if player gets a blackjack (21 points), claim winnings (doubled to account for original bet)
            check_for_blackjack(player)

            check_for_bust(player)

        # break out if they choose to stand
        if ans.upper() == "S":
            player_hitting = False

    # if player stands, play dealer's hand. Dealer will always hit until their value is >= 17

    print("Player stands. Dealer is playing...")

    print_hands(False)

    check_for_blackjack(dealer)

    while (dealer_hand_value < 17):
        dealer.hand.append(deck.deal())  # deal the dealer a card

        dealer_hand_value = dealer.update_hand_value()
        print_hands()

        check_for_blackjack(dealer)

        check_for_bust(dealer)

    # determine winner and adjust chips accordingly

    print(f"Dealer: {dealer_hand_value}")
    print(f"Player: {player_hand_value}")

    if (player_hand_value > dealer_hand_value):
        print("Player wins!")
        player.claim_winnings(bet * 2)
    elif (player_hand_value < dealer_hand_value):
        print("Dealer wins!")
    else:
        print("It's a draw!")
        # if there's a draw, return the player's bet
        player.claim_winnings(bet)

    print(f"You now have {player.chips} chips.")

    # ask player to play again


'''
TODOS

2. if player stands, play dealer's hand until >= 17. What if they bust?
make dealers hand show after player stands
3. Determine winner and adjust chips. DONT RUN THIS IF THE PLAYER BUSTS
4. make a loop to play again until they quit
5. adjust spacing/tabs to make interface look nicer
6. are there any ways to clean up my code?
7. consider adding comments to help myself and others understand the code
'''
