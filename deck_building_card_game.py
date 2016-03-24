import itertools
import random


class Card(object):
    def __init__(self, name, values=(0, 0), cost=1, clan=None):
        self.name = name
        self.cost = cost
        self.values = values
        self.clan = clan

    def __str__(self):
        return 'Name %s costing %s with attack %s and money %s' % \
               (self.name, self.cost, self.values[0], self.values[1])

    def get_attack(self):
        return self.values[0]

    def get_money(self):
        return self.values[1]


def card_init(player_one, player_computer, central):
    shared_deck_card = [4 * [Card('Archer', (3, 0), 2)],
                        4 * [Card('Baker', (0, 3), 2)],
                        3 * [Card('Swordsman', (4, 0), 3)],
                        2 * [Card('Knight', (6, 0), 5)],
                        3 * [Card('Tailor', (0, 4), 3)],
                        3 * [Card('Crossbowman', (4, 0), 3)],
                        3 * [Card('Merchant', (0, 5), 4)],
                        4 * [Card('Thug', (2, 0), 1)],
                        4 * [Card('Thief', (1, 1), 1)],
                        2 * [Card('Catapault', (7, 0), 6)],
                        2 * [Card('Caravan', (1, 5), 5)],
                        2 * [Card('Assassin', (5, 0), 4)]
                        ]
    player_one_deck = [8 * [Card('Serf', (0, 1), 0)],
                       2 * [Card('Squire', (1, 0), 0)]
                       ]
    player_computer_deck = [8 * [Card('Serf', (0, 1), 0)],
                            2 * [Card('Squire', (1, 0), 0)]
                            ]
    supplement = 10 * [Card('Levy', (1, 2), 2)]

    pod = list(itertools.chain.from_iterable(player_one_deck))
    player_one['deck'] = pod

    ptd = list(itertools.chain.from_iterable(player_computer_deck))
    player_computer['deck'] = ptd

    deck = list(itertools.chain.from_iterable(shared_deck_card))
    random.shuffle(deck)
    central['active'] = []
    central['supplement'] = supplement
    central['deck'] = deck

    max = central['active_size']
    count = 0
    while count < max:
        card = central['deck'].pop()
        central['active'].append(card)
        count = count + 1

    for x in range(0, player_one['handsize']):
        if len(player_one['deck']) == 0:
            random.shuffle(player_one['discard'])
            player_one['deck'] = player_one['discard']
            player_one['discard'] = []
        card = player_one['deck'].pop()
        player_one['hand'].append(card)

    for x in range(0, player_computer['handsize']):
        if len(player_computer['deck']) == 0:
            random.shuffle(player_computer['discard'])
            player_computer['deck'] = player_computer['discard']
            player_computer['discard'] = []
        card = player_computer['deck'].pop()
        player_computer['hand'].append(card)

    print_card_information(central)


def print_card_information(central):

    print("Available Cards")
    for card in central['active']:
        print(card)

    print("Supplement")
    if len(central['supplement']) > 0:
        print(central['supplement'][0])


def print_health(player_one, player_computer):
    print("\nPlayer Health %s" % player_one['health'])
    print("Computer Health %s" % player_computer['health'])


def act_play_all(money, attack, player_one):
    if len(player_one['hand']) > 0:
        for x in range(0, len(player_one['hand'])):
            card = player_one['hand'].pop()
            player_one['active'].append(card)
            money = money + card.get_money()
            attack = attack + card.get_attack()

    print("\nYour Hand")
    index = 0
    for card in player_one['hand']:
        print("[%s] %s" % (index, card))
        index = index + 1

    print("\nYour Active Cards")
    for card in player_one['active']:
        print(card)
    print("\nYour Values")
    print("Money %s, Attack %s" % (money, attack))
    return money, attack


def act_play_single_card(act, money, attack, player_one):
    if 1 <= int(act) <= len(player_one['hand']):
        player_one['active'].\
            append(player_one['hand'].pop(int(act) - 1))
        #for card in player_one['active']:
        money = money + player_one['active'][-1].get_money()
        attack = attack + player_one['active'][-1].get_attack()
    print("\nYour Hand")
    index = 1
    for card in player_one['hand']:
        print("[%s] %s" % (index, card))
        index = index + 1

    print("\nYour Active Cards")
    for card in player_one['active']:
        print(card)
    print("\nYour Values")
    print("Money %s, Attack %s" % (money, attack))
    return money, attack


def act_buy(money, player_one, central):
    while money > 0:
        print("Available Cards")
        ind = 1
        for card in central['active']:
            print("[%s] %s" % (ind, card))
            ind = ind + 1
        print("Choose a card to buy [1-n], S for supplement, "
              "E to end buying")
        bv = raw_input("Choose option: ")
        if bv == 'S':
            if len(central['supplement']) > 0:
                if money >= central['supplement'][0].cost:
                    money = money - central['supplement'][0].cost
                    player_one['discard'].\
                        append(central['supplement'].pop())
                    print("supplement Bought")
                else:
                    print("insufficient money to buy")
            else:
                print("no supplements left")
        elif bv == 'E':
            break
        elif bv.isdigit():
            if 1 <= int(bv) <= len(central['active']):
                if money >= central['active'][int(bv) - 1].cost:
                    money = money - \
                            central['active'][int(bv) - 1].cost
                    player_one['discard'].\
                        append(central['active'].pop(int(bv) - 1))
                    if len(central['deck']) > 0:
                        card = central['deck'].pop()
                        central['active'].insert(int(bv) - 1,card)
                    else:
                        central['active_size'] = \
                            central['active_size'] - 1
                    print("Card bought")
                else:
                    print("insufficient money to buy")
            else:
                print("enter a valid index number")
        else:
            print("Enter a valid option")
    return money


def act_attack(attack, player_computer):
    player_computer['health'] = player_computer['health'] - attack
    attack = 0
    return attack


def act_end(player_one):
    if len(player_one['hand']) > 0:
        for x in range(0, len(player_one['hand'])):
            player_one['discard'].append(player_one['hand'].pop())

    if len(player_one['active']) > 0:
        for x in range(0, len(player_one['active'])):
            player_one['discard'].append(player_one['active'].pop())
    for x in range(0, player_one['handsize']):
        if len(player_one['deck']) == 0:
            random.shuffle(player_one['discard'])
            player_one['deck'] = player_one['discard']
            player_one['discard'] = []
        card = player_one['deck'].pop()
        player_one['hand'].append(card)


def player_one_playing(player_one, player_computer, central):
    money = 0
    attack = 0
    game_over = False
    while True:
        print_health(player_one, player_computer)

        print("\nYour Hand")
        index = 1
        for card in player_one['hand']:
            print("[%s] %s" % (index, card))
            index = index + 1
        print("\nYour Values")
        print("Money %s, Attack %s" % (money, attack))
        print("\nChoose Action: (P = play all, "
              "[1-n] = play that card, B = Buy Card, "
              "A = Attack, E = end turn)")

        act = raw_input("Enter Action: ")
        print(act)
        if act == 'P':
            money, attack = act_play_all(money, attack, player_one)

        if act.isdigit():
            money, attack = \
                act_play_single_card(act, money, attack, player_one)

        if act == 'B':
            money = act_buy(money, player_one, central)

        if act == 'A':
            attack = act_attack(attack, player_computer)
            # judge the game result
            if player_computer['health'] <= 0:
                game_over = True
                break

        if act == 'E':
            act_end(player_one)
            break

        print("\n------------------------------------------------------")
    if game_over:
        print('Player One Wins')
    else:
        print_card_information(central)
        print_health(player_one, player_computer)

    return game_over


def player_computer_playing(player_one, player_computer, central):
    game_over = False
    money = 0
    attack = 0
    for x in range(0, len(player_computer['hand'])):
        card = player_computer['hand'].pop()
        player_computer['active'].append(card)
        money = money + card.get_money()
        attack = attack + card.get_attack()
    print(" Computer player values attack %s, money %s" % (attack, money))
    print(" Computer attacking with strength %s" % attack)

    player_one['health'] = player_one['health'] - attack
    attack = 0

    print_health(player_one, player_computer)

    if player_one['health'] <= 0:
        print("Computer wins")
        game_over = True
    else:
        print(" Computer player values attack %s, money %s" %
              (attack, money))

        print("Computer buying")
        if money > 0:
            cb = True
            templist = []
            print("Starting Money %s" % money)
            while cb:
                templist = []
                if len(central['supplement']) > 0:
                    if central['supplement'][0].cost <= money:
                        templist.append(("S", central['supplement'][0]))
                for int_index in range(0, central['active_size']):
                    if central['active'][int_index].cost <= money:
                        templist.\
                            append((int_index, central['active'][int_index]))
                if len(templist) > 0:
                    highest_index = 0
                    for int_index in range(0, len(templist)):
                        if templist[int_index][1].cost > \
                                templist[highest_index][1].cost:
                            highest_index = int_index
                        if templist[int_index][1].cost == \
                                templist[highest_index][1].cost:
                            if aggressive:
                                if templist[int_index][1].get_attack() >\
                                        templist[highest_index][1].get_attack():
                                    highest_index = int_index
                            else:
                                if templist[int_index][1].get_attack() >\
                                        templist[highest_index][1].get_money():
                                    highest_index = int_index
                    source = templist[highest_index][0]
                    if source in range(0, 5):
                        if money >= central['active'][int(source)].cost:
                            money = money - \
                                    central['active'][int(source)].cost
                            card = central['active'].pop(int(source))
                            print "Card bought %s" % card
                            player_computer['discard'].append(card)
                            if len(central['deck']) > 0:
                                card = central['deck'].pop()
                                central['active'].append(card)
                            else:
                                central['active_size'] = \
                                    central['active_size'] - 1
                        else:
                            print "Error Occurred"
                    else:
                        if money >= central['supplement'][0].cost:
                            money = money - central['supplement'][0].cost
                            card = central['supplement'].pop()
                            player_computer['discard'].append(card)
                            print "Supplement Bought %s" % card
                        else:
                            print "Error Occurred"
                else:
                    cb = False
                if money == 0:
                    cb = False
        else:
            print("No Money to buy anything")

        if len(player_computer['hand']) > 0:
            for x in range(0, len(player_computer['hand'])):
                player_computer['discard'].\
                    append(player_computer['hand'].pop())
        if len(player_computer['active']) > 0:
            for x in range(0, len(player_computer['active'])):
                player_computer['discard'].\
                    append(player_computer['active'].pop())
        for x in range(0, player_computer['handsize']):
            if len(player_computer['deck']) == 0:
                random.shuffle(player_computer['discard'])
                player_computer['deck'] = player_computer['discard']
                player_computer['discard'] = []
            card = player_computer['deck'].pop()
            player_computer['hand'].append(card)
        print("Computer turn ending")

        print_card_information(central)
        print_health(player_one, player_computer)

    return game_over


def game(player_one, player_computer, central):
    game_over = False
    while 1:
        print("====player playing start===============================")
        game_over = player_one_playing(player_one, player_computer, central)
        print("====player playing finish==============================\n")
        if game_over:
            break

        print("====computer playing start=============================")
        game_over = \
            player_computer_playing(player_one, player_computer, central)
        print("====computer playing finish============================\n")
        if game_over:
            break
    return game_over


def judgement(player_one, player_computer, central):
    if central['active_size'] == 0:
        print("No more cards available")
    if player_one['health'] > player_computer['health']:
        print("Player One Wins on Health")
    elif player_computer['health'] > player_one['health']:
        print("Computer Wins on Health")
    else:
        player_one_strength = 0
        player_computer_strength = 0
        for card in player_one['hand']:
            player_one_strength = player_one_strength + card.get_attack
        for card in player_computer['hand']:
            player_computer_strength = player_computer_strength + \
                                       card.get_attack
        if player_one_strength > player_computer_strength:
            print("Player One Wins on Card Strength")
        elif player_computer_strength > player_one_strength:
            print("Computer Wins on Card Strength")
        else:
            print("Draw")


if __name__ == '__main__':

    pG = raw_input('Do you want to play a game?(Y/N):')
    cG = (pG=='Y')

    while cG:
        oT = raw_input("Do you want an aggressive (A) opponent or "
                       "an acquisative (any key except A) opponent:")
        aggressive = (oT == 'A')

        player = {'name': 'player one', 'health': 30, 'deck': [], 'hand': [],
                  'active': [], 'handsize': 5, 'discard': []}
        computer = {'name': 'player computer', 'health': 30, 'deck': [],
                    'hand': [], 'active': [], 'handsize': 5, 'discard': []}
        central_line = {'name': 'central', 'active': [], 'active_size': 5,
                        'supplement': [], 'deck': []}

        card_init(player, computer, central_line)

        cG = game(player, computer, central_line)
        if not cG:
            pG = raw_input('Do you want to play another game?(Y/N):')
            cG = (pG=='Y')
            continue

        judgement(player, computer, central_line)

        cG = False
        pG = raw_input('Do you want to play another game?(Y/N):')
        cG = (pG=='Y')
    exit()
