import pypokerengine
from pypokerengine.api.game import setup_config, start_poker
from pypokerengine.utils.card_utils import gen_cards, _montecarlo_simulation
from fish import FishPlayer
from user import ConsolePlayer
from randomp import RandomPlayer
import random

config = setup_config(max_round=1, initial_stack=1000, small_blind_amount=20)
config.register_player(name="f1", algorithm=FishPlayer())
config.register_player(name="f2", algorithm=FishPlayer())
config.register_player(name="r2", algorithm=RandomPlayer())
config.register_player(name="c1", algorithm=ConsolePlayer())

def calculate(nb_simulation, nb_player, hole_card, amount_to_call, pot_size, stack_size, pre_flop_aggressor, table_tightness, community_card=None):
    if not community_card: community_card = []
    win_count = sum([_montecarlo_simulation(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
    equity = 1.0 * win_count / nb_simulation
    pot_odds = amount_to_call / (pot_size + amount_to_call)
    if pot_odds > equity + 0.25:
        print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Fold")
    elif pot_odds < equity - 0.25:
        if 2 * amount_to_call > stack_size:
            print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Go all in!")
        else:
            random_raise_multiplier = random.randint(25, 35) / 10
            amount_to_raise = int(amount_to_call * random_raise_multiplier)
            print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Raise to: " + str(amount_to_raise))
    else:
        if pre_flop_aggressor == True and table_tightness == True:
            print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Fold, you have marginal equity but the table is tight and people know you're the pre-flop aggressor")
        elif pre_flop_aggressor == False and table_tightness == False:
            print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Call, you have marginal equity but the table is loose and you're not the pre-flop aggressor")
        else:
            decision_maker = random.randint(0, 1)
            if decision_maker == 0:
                print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Call, you have marginal equity and the other factors make for a contradicting decision. So the randomizer said to call.")
            else:
                print("Equity: " + str(equity) + " Pot odds: " + str(pot_odds) + ". Fold, you have marginal equity and the other factors make for a contradicting decision. So the randomizer said to fold.")

hole_card = gen_cards(['H4', 'D7'])
community_card = gen_cards(['D3', 'C5', 'C6', 'SK', 'C4'])
pot_size = 100
amount_to_call = 30
stack_size = 1000
pre_flop_aggressor = True
table_tightness = False
calculate(nb_simulation=1000, nb_player=3, hole_card=hole_card, amount_to_call = amount_to_call, pot_size = pot_size, stack_size = stack_size, pre_flop_aggressor = pre_flop_aggressor, table_tightness = table_tightness, community_card=community_card)

