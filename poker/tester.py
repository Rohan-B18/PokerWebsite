import pypokerengine
from pypokerengine.api.game import setup_config, start_poker
from pypokerengine.utils.card_utils import gen_cards, _montecarlo_simulation, _fill_community_card, _pick_unused_card
import random
from pypokerengine.engine.card import Card
from pypokerengine.engine.deck import Deck
from pypokerengine.engine.hand_evaluator import HandEvaluator

def calculate(nb_simulation, nb_player, hole_card, amount_to_call, pot_size, stack_size, pre_flop_aggressor, table_tightness, community_card=None):
    if not community_card: community_card = []
    win_count = sum([_montecarlo_simulation(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
    equity = 1.0 * win_count / nb_simulation
    pot_odds = amount_to_call / (pot_size + amount_to_call)
    if pot_odds > equity + 0.25:
        return 2
        print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Fold")
    elif pot_odds < equity - 0.25:
        if 2 * amount_to_call > stack_size:
            return 3
            print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Go all in!")
        else:
            random_raise_multiplier = random.randint(25, 35) / 10
            amount_to_raise = int(amount_to_call * random_raise_multiplier)
            return 4
            print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Raise to: " + str(amount_to_raise))
    else:
        if pre_flop_aggressor == True and table_tightness == True:
            return 2
            print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Fold, you have marginal equity but the table is tight and people know you're the pre-flop aggressor")
        elif pre_flop_aggressor == False and table_tightness == False:
            return 5
            print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Call, you have marginal equity but the table is loose and you're not the pre-flop aggressor")
        else:
            decision_maker = random.randint(0, 1)
            if decision_maker == 0:
                return 6
                print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Call, you have marginal equity and the other factors make for a contradicting decision. So the randomizer said to call.")
            else:
                return 6
                print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Fold, you have marginal equity and the other factors make for a contradicting decision. So the randomizer said to fold.")

# Create a deck of cards and shuffle it
deck = Deck()
deck.shuffle()

hole_cards = deck.draw_cards(2)
community_cards = deck.draw_cards(3)
hole_card_list = [str(card) for card in hole_cards]
community_card_list = [str(card) for card in community_cards]
hole_card = gen_cards(hole_card_list)
community_card = gen_cards(community_card_list)
print(hole_card_list)
print(community_card_list)

pot_size = random.randint(50, 500)
amount_to_call = random.randint(50, pot_size)
stack_size = random.randint(250, 1250)
pre_flop_aggressor = random.randint(0, 1)
table_tightness = random.randint(0, 1)
user_input = int(input())
value = calculate(nb_simulation=1000, nb_player=3, hole_card=hole_card, amount_to_call = amount_to_call, pot_size = pot_size, stack_size = stack_size, pre_flop_aggressor = pre_flop_aggressor, table_tightness = table_tightness, community_card=community_card)
print(value)