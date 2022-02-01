from api import State
from api import Deck
from api import util
import random


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # Phase 1
        # phase = State.get_phase(self)
        moves = state.moves()
        hand = state.hand()
        print (moves)
        
        def phase_1():

            

            def check_marriage():

                kings_and_queens = []

                for card in hand:
                    rank_of_the_card = util.get_rank(card)
                    if rank_of_the_card == "Q" or rank_of_the_card == "K":
                        kings_and_queens.append(card)

                for [card1, card2] in kings_and_queens:
                    if card1 is not None and card2 is not None:
                        # Getpoints player 1 or not player 1's turn
                        if util.get_points(1) < 26 or opponent_lead() == True:
                            moves.remove(card1, card2)
                        else:
                            return [card1, card2]

            def opponent_lead():
                if state.whose_turn == 2:
                    return True

            def ourbot_lead():
                if state.whose_turn == 1:
                    return True

            # should maybe be outside of get_move?
            # don't need/maybe if we want to incoorporate the 'adjacent' cards strategy
            def store_played_cards():
                played_cards = []
                played_cards += state.get_opponents_played_card()
                played_cards += chosen_move

            def what_suit_is_trump():
                suit_of_trump = state.get_trump_suit()
                return suit_of_trump

            def trump_cards_in_hand():
                trump_cards_in_hand = []
                for card in hand:
                    if util.get_suit(card) == what_suit_is_trump():
                        trump_cards_in_hand.append(card)

            def play_non_trump_low_rank():
                for card in moves:
                    if util.get_suit(card) != what_suit_is_trump():
                        chosen_move = None
                        if util.get_rank(card) == 'A':
                            chosen_move = card
                        elif util.get_rank(card) == '10':
                            chosen_move = card
                        elif util.get_rank(card) == 'K':
                            chosen_move = card
                        elif util.get_rank(card) == 'Q':
                            chosen_move = card
                        elif util.get_rank(card) == 'J':
                            chosen_move = card
                        return chosen_move

            def play_non_trump_high_rank():
                for card in moves:
                    if util.get_suit(card) != what_suit_is_trump():
                        chosen_move = None
                        if util.get_rank(card) == 'J':
                            chosen_move = card
                        elif util.get_rank(card) == 'Q':
                            chosen_move = card
                        elif util.get_rank(card) == 'K':
                            chosen_move = card
                        elif util.get_rank(card) == '10':
                            chosen_move = card
                        elif util.get_rank(card) == 'A':
                            chosen_move = card
                        return chosen_move

            def opponent_leads_high_rank_non_trump():
                chosen_move = None
                for card in trump_cards_in_hand():
                    chosen_move = card
                    if util.get_rank(chosen_move) < util.get_rank(card):
                        chosen_move = card
                    else:
                        chosen_move = play_non_trump_low_rank()
                return chosen_move

            def opponent_leads_low_rank_non_trump():
                chosen_move = play_non_trump_high_rank()
                return chosen_move

            def opponent_leads_trump():
                chosen_move = play_non_trump_low_rank()
                return chosen_move

            def ourbout_leads():
                if ourbot_lead() == True:
                    chosen_move = play_non_trump_low_rank()
                    return chosen_move

            check_marriage()

            # game logic phase 1
            if opponent_lead() == True:
                opponent_played = state.get_opponents_played_card()
                if util.get_suit(opponent_played) != what_suit_is_trump():
                    if util.get_rank(opponent_played) == "A" or util.get_rank(opponent_played) == "10":
                        chosen_move = opponent_leads_high_rank_non_trump()
                    else:
                        chosen_move = opponent_leads_low_rank_non_trump()
                else:
                    chosen_move = opponent_leads_trump()
            else:
                chosen_move = ourbout_leads()

            if chosen_move is not None:
                print (moves)
                return chosen_move
            else:
                return random.choice(moves)

    phase = State.get_phase
    # if phase == 1:
# trying without minimax
# get_move()

# else:

#  get_move2()


# Phase 2 (minimax)

# Literal minimax copy, may need work

def phase_2(self):
    __max_depth = -1
    __randomize = True

    def __init__(self, randomize=True, depth=6):
        """
        :param randomize: Whether to select randomly from moves of equal value (or to select the first always)
        :param depth:
        """
        self.__randomize = randomize
        self.__max_depth = depth

    def get_move(self, state):
        # type: (State) -> tuple[int, int]

        val, move = self.value(state)

        return move

    def value(self, state, depth=0):
        # type: (State, int) -> tuple[float, tuple[int, int]]
        """
        Return the value of this state and the associated move
        :param state:
        :param depth:
        :return: A tuple containing the value of this state, and the best move for the player currently to move
        """

        if state.finished():
            winner, points = state.winner()
            return (points, None) if winner == 1 else (-points, None)

        if depth == self.__max_depth:
            return heuristic(state)

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        for move in moves:

            next_state = state.next(move)

            value, _ = self.value(next_state)

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        return best_value, best_move


def maximizing(state):
    # type: (State) -> bool
    """
    Whether we're the maximizing player (1) or the minimizing player (2).

    """
    return state.whose_turn() == 1


def heuristic(state):
    # type: (State) -> float
    """
    Estimate the value of this state: -1.0 is a certain win for player 2, 1.0 is a certain win for player 1

    :param state:
    :return: A heuristic evaluation for the given state (between -1.0 and 1.0)
    """
    return util.ratio_points(state, 1) * 2.0 - 1.0, None