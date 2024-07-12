from dataclasses import dataclass, field
from typing import List, Callable

from core import GameState, Player


class Game:
    """Class for keeping track of game play."""
    players: List[Player]
    game_state: GameState
    current_turn: int = 0
    
    def __init__(self, word:str, playerNames: List[str]):
        self.current_turn = 0
        self.game_state = GameState(word)

        self.players = [None] * len(playerNames)
        for idx, name in enumerate(playerNames):
            self.players[idx] = Player(name)
    
    def move_to_next_player(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def turn(self) -> bool:
        current_player = self.players[self.current_turn]
        gameFinished = self.turn_logic(current_player, self.game_state)
        if not gameFinished:
            self.move_to_next_player()
        
        return gameFinished
    
    def play(self):
        gameFinished = False
        while(not gameFinished):
            gameFinished = self.turn()

    def print_stats(self):
        stats = "================================["
        stats += " ".join(f"{player.name}: {player.score}" for player in self.players)
        stats += f"]================================{list(self.game_state.guessed_letters)}============"
        print(stats)
    
    def turn_logic(self, player: Player, state: GameState) -> bool:
        print(f"It's {player.name}'s turn, current score: {player.score}, if you want to type the whole word - enter *<word>")
        state.print_current_state()

        while True:
            guess = input("Guess a letter: ").lower()

            if guess in state.guessed_letters:
                print("You already guessed that letter. Try again.")
                continue

            if self.process_guess(guess, player, state):
                return True

            self.print_stats()
            if guess not in state.word:
                break

        return False

    def process_guess(self, guess: str, player: Player, state: GameState) -> bool:
        if guess[0] == '*' and guess[1:] == state.word:
            return self.process_full_word_guess(player, state)

        state.guessed_letters.add(guess)

        if guess in state.word:
            return self.process_correct_letter_guess(player, state)

        return False

    def process_full_word_guess(self, player: Player, state: GameState) -> bool:
        diff = set(state.word) - state.guessed_letters
        state.guessed_letters.update(diff)
        player.update_score(len(diff))
        print(f"Congratulations! You guessed the word '{state.word}'.")
        self.print_stats()
        return True

    def process_correct_letter_guess(self, player: Player, state: GameState) -> bool:
        player.update_score()
        if set(state.word) <= state.guessed_letters:
            print(f"Congratulations! You guessed the word '{state.word}'.")
            return True
        print("You got it right!, if you want to type the whole word - enter *<word>")
        state.print_current_state()
        return False