import deck_building_card
import unittest


class CardTestCase(unittest. TestCase):
    def test_name(self):
        name = deck_building_card.Card('Archer', (3, 0), 2).name
        self.assertEqual("Archer", name)

    def test_cost(self):
        cost = deck_building_card.Card('Archer', (3, 0), 2).cost
        self.assertEqual(2, cost)

    def test_attack(self):
        attack = deck_building_card.Card('Archer', (3, 0), 2).get_attack()
        self.assertEqual(3, attack)

    def test_money(self):
        money = deck_building_card.Card('Archer', (3, 0), 2).get_money()
        self.assertEqual(0, money)


class CardInitTestCase(unittest. TestCase):
    def player_deck(self):
        # test the player deck contains cards
        player1 = {'name': 'player one', 'health': 30, 'deck': [1,1,1],
                   'hand': [], 'active': [], 'handsize': 5, 'discard': []}
        player2 = {'name': 'player computer', 'health': 30, 'deck': [],
                    'hand': [], 'active': [], 'handsize': 5, 'discard': []}
        central = {'name': 'central', 'active': [], 'active_size': 5,
                        'supplement': [], 'deck': []}
        deck_building_card.card_init(player1, player2, central)
        self.assertIsInstance(deck_building_card.Card, player1['deck'])

    def computer_deck(self):
        # test the computer deck contains cards
        player1 = {'name': 'player one', 'health': 30, 'deck': [], 'hand': [],
                  'active': [], 'handsize': 5, 'discard': []}
        player2 = {'name': 'player computer', 'health': 30, 'deck': [1,1,1],
                    'hand': [], 'active': [], 'handsize': 5, 'discard': []}
        central = {'name': 'central', 'active': [], 'active_size': 5,
                        'supplement': [], 'deck': []}
        deck_building_card.card_init(player1, player2, central)
        self.assertIsInstance(deck_building_card.Card, player2['deck'])

    def central_deck(self):
        # test the main deck contains cards
        player1 = {'name': 'player one', 'health': 30, 'deck': [], 'hand': [],
                  'active': [], 'handsize': 5, 'discard': []}
        player2 = {'name': 'player computer', 'health': 30, 'deck': [],
                    'hand': [], 'active': [], 'handsize': 5, 'discard': []}
        central = {'name': 'central', 'active': [], 'active_size': 5,
                        'supplement': [], 'deck': [1,1,1]}
        deck_building_card.card_init(player1, player2, central)
        self.assertIsINstance(central['deck'][0], deck_building_card.Card)

    def test_player_discard(self):
        player1 = {'name': 'player one', 'health': 30, 'deck': [], 'hand': [],
                   'active': [], 'handsize': 5, 'discard': []}
        player2 = {'name': 'player computer', 'health': 30, 'deck': [],
                    'hand': [], 'active': [], 'handsize': 5, 'discard': []}
        central = {'name': 'central', 'active': [], 'active_size': 5,
                        'supplement': [], 'deck': []}
        deck_building_card.card_init(player1, player2, central)
        self.assertEqual([], player1['discard'])

    def test_computer_discard(self):
        player1 = {'name': 'player one', 'health': 30, 'deck': [], 'hand': [],
                  'active': [], 'handsize': 5, 'discard': []}
        player2 = {'name': 'player computer', 'health': 30, 'deck': [],
                   'hand': [], 'active': [], 'handsize': 5, 'discard': []}
        central = {'name': 'central', 'active': [], 'active_size': 5,
                        'supplement': [], 'deck': []}
        deck_building_card.card_init(player1, player2, central)
        self.assertEqual([], player2['discard'])


class PlayAllTestCase(unittest. TestCase):
    def test_player_get_value(self):
        # test the change of money and attack values
        money = 0
        attack =0
        player1 = {'name': 'player one', 'health': 30, 'deck': [],
                   'hand': [deck_building_card.Card('Archer', (3, 0), 2)],
                   'active': [], 'handsize': 5, 'discard': []}
        money, attack = deck_building_card.\
            act_play_all(money, attack, player1)
        self.assertEqual((3, 0), (attack, money))

    def test_hand(self):
        # test the hand is empty
        money = 0
        attack =0
        player1 = {'name': 'player one', 'health': 30, 'deck': [],
                   'hand': [deck_building_card.Card('Archer', (3, 0), 2)],
                   'active': [], 'handsize': 5, 'discard': []}
        deck_building_card.act_play_all(money, attack, player1)
        self.assertEqual([], player1['hand'])


class PlaySingleTestCase(unittest. TestCase):
    def test_out_range_input(self):
        # input value out of the number of hand cards
        act = 3
        money = 0
        attack = 0
        player1 = {'name': 'player one', 'health': 30, 'deck': [],
                   'hand': [deck_building_card.Card('Archer', (3, 0), 2)],
                   'active': [], 'handsize': 5, 'discard': []}
        money, attack = \
            deck_building_card.\
                act_play_single_card(act, money, attack, player1)
        self.assertEqual(1, len(player1['hand']))

    def test_correct_input(self):
        act = 1
        money = 0
        attack = 0
        player1 = {'name': 'player one', 'health': 30, 'deck': [],
                   'hand': [deck_building_card.Card('Archer', (3, 0), 2)],
                   'active': [], 'handsize': 5, 'discard': []}
        money, attack = \
            deck_building_card.\
                act_play_single_card(act, money, attack, player1)
        self.assertEqual([], player1['hand'])

    def test_player_get_value(self):
        # change of money and attack
        act = 1
        money = 0
        attack = 0
        player1 = {'name': 'player one', 'health': 30, 'deck': [],
                   'hand': [deck_building_card.Card('Archer', (3, 0), 2)],
                   'active': [], 'handsize': 5, 'discard': []}
        money, attack = \
            deck_building_card.\
                act_play_single_card(act, money, attack, player1)
        self.assertEqual((3, 0), (attack, money))


class AttackTestCase(unittest. TestCase):
    def test_player_attack(self):
        # opponent's health
        attack = 1
        player2 = {'name': 'player computer', 'health': 30, 'deck': [],
                   'hand': [], 'active': [], 'handsize': 5, 'discard': []}
        deck_building_card.act_attack(attack, player2)
        self.assertEqual(29, player2['health'])


class EndTestCase(unittest. TestCase):
    def test_empty_active(self):
        # remove all the cards in active area
        player1 = {'name': 'player one', 'health': 30,
                   'deck': 10 * [deck_building_card.Card('Archer', (3, 0), 2)],
                   'hand': [],
                   'active': [deck_building_card.Card('Archer', (3, 0), 2)],
                   'handsize': 5, 'discard': []}
        deck_building_card.act_end(player1)
        self.assertEqual([], player1['active'])

    def test_new_hand(self):
        # get new hand cards
        player1 = {'name': 'player one', 'health': 30,
                   'deck': 2 * [deck_building_card.Card('Baker', (3, 0), 2)],
                   'hand': [deck_building_card.Card('Archer', (3, 0), 2)],
                   'active': [], 'handsize': 2, 'discard': []}
        deck_building_card.act_end(player1)
        self.assertEqual(2, len(player1['hand']))


class GameOverTestCase(unittest. TestCase):
    def test_game_over(self):
        # game over when players health reduce to zero
        game_over = False
        player1 = {'name': 'player one', 'health': -1, 'deck': [],
            'hand': [], 'active': [], 'handsize': 5, 'discard': []}
        player2 = {'name': 'player computer', 'health': 0, 'deck': [],
            'hand': [], 'active': [], 'handsize': 5, 'discard': []}
        central = {'name': 'central', 'active': [], 'active_size': 5,
                        'supplement': [], 'deck': []}
        game_over = deck_building_card.\
                player_computer_playing(player1, player2, central)
        self.assertTrue(game_over)


if __name__ == "__main__":
    unittest.main()