hangman cmdline game

*************Welcome to Hangman!***********
usage: Hangman [-h] [-f FILENAME] [-p PLAYERS] -c COUNT

guess words to win the game

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
  -p PLAYERS, --players PLAYERS
  -c COUNT, --count COUNT
                        an integer for the number of random words from the
                        file
                        
for a game of 2 words, 3 players:
usage: python3 hangmanGame.py -f ./words.txt -c 2 -p 3 

