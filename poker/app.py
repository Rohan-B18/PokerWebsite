import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import pypokerengine
from pypokerengine.api.game import setup_config, start_poker
from pypokerengine.utils.card_utils import gen_cards, _montecarlo_simulation
from pypokerengine.engine.deck import Deck
import random

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("You must provide a username", 400)
        elif not password:
            return apology("You must provide a password", 400)
        elif not confirmation:
            return apology("You must confirm your password", 400)
        elif password != confirmation:
            return apology("Passwords must match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username not already exists
        if len(rows) != 0:
            return apology("username already exists")

        # Insert new user into database
        user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                             username=request.form.get("username"),
                             hash=generate_password_hash(request.form.get("password")))

        # Remember which user has logged in
        session["user_id"] = user_id

        # Redirect user to home page
        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/calculator", methods=["GET", "POST"])
@login_required
def calculate():
    if request.method == "POST":

        # Stores all of the information in the form into variables
        amount_to_call = int(request.form.get("amount_to_call"))
        pot_size = int(request.form.get("pot_size"))
        stack_size = int(request.form.get("stack_size"))
        pre_flop_aggressor = int(request.form.get("pre_flop_aggressor"))
        table_tightness = int(request.form.get("table_tightness"))
        nb_simulation = int(request.form.get("nb_simulation"))
        nb_player = int(request.form.get("nb_player"))
        hole_cards = str(request.form.get("hole_card1"))
        hole_card_list = list(hole_cards.split(" "))
        hole_card = gen_cards(hole_card_list)
        community_cards = str(request.form.get("community_card1"))
        community_card_list = list(community_cards.split(" "))
        community_card = gen_cards(community_card_list)

        # Simulate many hands using montecarlo simulator from pypokerengine
        win_count = sum([_montecarlo_simulation(nb_player, hole_card, community_card) for i in range(nb_simulation)])
        equity = 1.0 * win_count / nb_simulation
        pot_odds = amount_to_call / (pot_size + amount_to_call)

        # Make decision based on equity, pot odds, stack size, and other factors from the form
        if pot_odds > equity + 0.25:
            decision = "Fold"
        elif pot_odds < equity - 0.25:
            if 2 * amount_to_call > stack_size:
                decision = "Go all in!"
            else:
                random_raise_multiplier = random.randint(25, 35) / 10
                amount_to_raise = int(amount_to_call * random_raise_multiplier)
                decision = "Raise to " + str(amount_to_raise)
        else:
            if pre_flop_aggressor == True and table_tightness == True:
                decision = "Fold, you have marginal equity but the table is tight and people know you're the pre-flop aggressor"
            elif pre_flop_aggressor == False and table_tightness == False:
                decision = "Call, you have marginal equity but the table is loose and you're not the pre-flop aggressor"
            else:
                decision_maker = random.randint(0, 1)
                if decision_maker == 0:

                    decision = "Call, you have marginal equity and the other factors make for a contradicting decision. So the randomizer said to call."
                else:
                    decision = "Fold, you have marginal equity and the other factors make for a contradicting decision. So the randomizer said to fold."

        return render_template("result.html", decision=decision, equity=equity, pot_odds=pot_odds)
    else:
        return render_template("calculator.html")

# Create a deck of cards and shuffle it
deck = Deck()
deck.shuffle()
hole_cards = deck.draw_cards(2)
community_cards = deck.draw_cards(3)
hole_card_list = [str(card) for card in hole_cards]
community_card_list = [str(card) for card in community_cards]
hole_card = gen_cards(hole_card_list)
community_card = gen_cards(community_card_list)
pot_size = random.randint(50, 500)
amount_to_call = random.randint(50, pot_size)
stack_size = random.randint(250, 1250)
pre_flop_aggressor = random.randint(0, 1)
table_tightness = random.randint(0, 1)

@app.route("/tester", methods=["GET", "POST"])
@login_required
def tester():
    if request.method == "POST":
        def calculate(nb_simulation, nb_player, hole_card, amount_to_call, pot_size, stack_size, pre_flop_aggressor, table_tightness, community_card=None):
            if not community_card: community_card = []
            win_count = sum([_montecarlo_simulation(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
            equity = 1.0 * win_count / nb_simulation
            pot_odds = amount_to_call / (pot_size + amount_to_call)
            if pot_odds > equity + 0.25:
                return 1
            elif pot_odds < equity - 0.25:
                if 2 * amount_to_call > stack_size:
                    return 2
                else:
                    random_raise_multiplier = random.randint(25, 35) / 10
                    amount_to_raise = int(amount_to_call * random_raise_multiplier)
                    return 3
            else:
                if pre_flop_aggressor == True and table_tightness == True:
                    return 4
                elif pre_flop_aggressor == False and table_tightness == False:
                    return 5
                else:
                    return 6

        value = calculate(nb_simulation=1000, nb_player=3, hole_card=hole_card, amount_to_call = amount_to_call, pot_size = pot_size, stack_size = stack_size, pre_flop_aggressor = pre_flop_aggressor, table_tightness = table_tightness, community_card=community_card)
        user_input = int(request.form.get("user_input"))
        if value == user_input:
            flash("Correct!")
        else:
            flash("Incorrect!")

        return redirect("/tester")

    else:
        return render_template("tester.html", hole_card_list = hole_card_list, community_card_list = community_card_list, pot_size = pot_size, amount_to_call = amount_to_call, stack_size = stack_size, pre_flop_aggressor = pre_flop_aggressor, table_tightness = table_tightness)


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/tipsandtricks")
@login_required
def tipsandtricks():
    return render_template("tipsandtricks.html")

@app.route("/guide")
@login_required
def guide():
    return render_template("guide.html")

@app.route("/quiz")
@login_required
def quiz():
    return render_template("quiz.html")