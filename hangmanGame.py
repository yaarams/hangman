from random import choice, sample
import argparse
from typing import List

from core import Player
from game import Game

class GameInitiator:
    """Class for initiating the game."""

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(
                        prog='Hangman',
                        description='guess words to win the game',
                        epilog='Text at the bottom of help')
        parser.add_argument('-f', '--filename', type=str, default="./words.txt")          
        parser.add_argument('-p', '--players', type=int, default=2)
        parser.add_argument('-c', '--count', type=int, default=15,
                            help='an integer for the number of random words from the file')
        return parser.parse_args()

    @staticmethod
    def select_words(filename: str, count: int = 15):
        """
        Returns a list of words - lowercase letters.
        The default amout of words is 15, this function may take a while to finish.
        """
        with open(filename, mode="r") as words:
            word_list = words.readlines()
        words = [word.strip().lower() for word in word_list]
        return sample(words, count)


class GamesRunner:
    """Class for running games and keeping track of winners."""
    words: List[str]

    games_count: int
    games_index: int = 0

    players_count: int    
    player_names: List[str]
    players_scores: List[int] 

    def __init__(self):
        print(f"*************Welcome to Hangman!***********")
        initiator = GameInitiator()
        args = initiator.parse_args()
        self.words = initiator.select_words(args.filename, args.count)
        self.games_count = args.count # amount of games / random words

        self.players_count = args.players # amount of players
        self.players_scores = [0] * self.players_count
        self.player_names = [""] * self.players_count

        for x in range(self.players_count):
            self.player_names[x] = input(f"#{x+1} player name: ").lower()

    def update_winner(self, game: Game):
        self.games_index += 1
        winner_index, winner = max(enumerate(game.players), key=lambda x: x[1].score)
        print(f"{winner.name} - You Won!")
        self.players_scores[winner_index] += 1

    def print_scores(self, game):
        scores = " ".join(f"{player.name}'s score: {self.players_scores[idx]}" for idx, player in enumerate(game.players))
        print(scores)
    
    def print_stats(self, game: Game):
        stats = f"================================{self.games_index}/{self.games_count}======================scores:["
        stats += " ".join(f"{player.name}: {self.players_scores[idx]}" for idx, player in enumerate(game.players))
        stats += "]"
        print(stats)

    def run_games(self):
        while(self.games_index < self.games_count):
            word = choice(self.words)
            game = Game(word, self.player_names)
            self.print_stats(game)
            game.play()
            self.update_winner(game)
            self.print_scores(game)

        print(f"Hangman games has ended!")

def main():
    runner = GamesRunner()
    runner.run_games()

if __name__ == "__main__":
    main()