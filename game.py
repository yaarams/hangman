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
    
    def next(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def turn(self):
        current_player = self.players[self.current_turn]
        gameFinished = self.turnLogic(current_player, self.game_state)
        if not gameFinished:
            self.next() # Move to the next player's turn
        
        return gameFinished
    
    def play(self):
        gameFinished = False
        while(not gameFinished):
            gameFinished = self.turn()

    def printStats(self):
        stats = "================================["
        for x in range(len(self.players)):
            stats += f"{self.players[x].name}: {self.players[x].score} "
        stats += f"]================================{list(self.game_state.guessed_letters)}============"
        print(stats)
    
    # this logic can basically be external to the game
    def turnLogic(self, player: Player, state: GameState):
        print(f"It's {player.name}'s turn, current score: {player.score}, if you want to type the whole word - enter *<word>")
        
        state.printCurrentState()
        newGuess = False
    
        while not newGuess:
            guess = input("Guess a letter: ").lower()

            if guess in state.guessed_letters:
                print("You already guessed that letter. Try again.")
            
            else:
                newGuess = True
                state.guessed_letters.add(guess)

                if guess in state.word:
                    player.updateScore()

                    if set(state.word) <= state.guessed_letters:
                        print(f"Congratulations! You guessed the word '{state.word}'.")
                        return True
                    
                    print(f"You got it right!, if you want to type the whole word - enter *<word>")
                    state.printCurrentState()
                    newGuess = False

                elif guess[0] == "*" and guess[1:] == state.word:
                    player.updateScore()
                    print(f"Congratulations! You guessed the word '{state.word}'.")
                    return True
                
            self.printStats()
                
        return False