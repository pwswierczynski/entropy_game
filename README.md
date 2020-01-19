# Entropy Board Game

## Introduction
This is an implementation of Entropy board game  designed by Eric Solomon in 1977. For the rules of the game see: https://en.wikipedia.org/wiki/Entropy_(1977_board_game)

## Installation
The game is written in Python 3.7 and is not compatible with Python 2.x.

Make sure you are in a virtual environment. To create one use:
'''
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate
'''

To install the required Python packages, navigate to the main repo directory and call
'''
pip install -r requirements.txt
'''

To make sure your PYTHONPATH is set correctly, you can call
'''
export PYTHONPATH=.
'''

To play a game, call
' python examples/play_entropy.py'

## To Do
* Create a more appealing GUI
* Create an AI engine for asymmetric game with complete information
