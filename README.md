# Rock Paper Scissors Project

- Programmer: Matin Saadatii
    - LinkedIn: https://www.linkedin.com/in/matin-saadatii/
    - Site: https://matechs.ir
    - Telegram: https://t.me/sMATINss
- Description: Implement the "Rock Paper Scissors" game with Python

## Features

- Play against the computer for as many sets as you want.
- Ties don't count: a tied round is simply replayed, so you always get exactly the number of sets you asked for.
- Input is validated: the number of sets must be a positive whole number, and choices are case-insensitive (`Rock`, ` PAPER `, etc. are accepted).
- The computer's choice is shown after every round.
- A final result message shows the winner and the score (or a tie).

## Requirements

- Python 3.8 or newer
- No external packages (only the standard library: `random`, `typing`)

## How to Run

```bash
python src/rock_paper_scissors.py
```

The program asks for your name and the number of sets, then asks for your choice every round.

### Example session

```
Enter your name: Matin
Enter the number of sets you want to play: 2
Enter your choice (rock, paper, scissors): rock
Computer chose scissors.
Matin wins! rock beats scissors.
Enter your choice (rock, paper, scissors): paper
Computer chose paper.
It's a tie! Both players chose paper. Please play again.
Enter your choice (rock, paper, scissors): scissors
Computer chose rock.
Computer wins! rock beats scissors.
The game is a tie with a score of 1 to 1!
```

## Implementation

The game has two main classes: `RockPaperScissorsPlayer` and `RockPaperScissorsGame`.

### The `RockPaperScissorsPlayer`

This class has four attributes: `name`, `choice`, `winner`, and `score`.

Each of these attributes is changed through a small setter-style method: `make_choice`, `set_winner`, and `increase_score`.

```python
def make_choice(self, choice: str):
    """Sets the player's choice to the given choice."""
    self.choice = choice
```

| Method | Description |
| --- | --- |
| `make_choice(choice)` | Stores the player's current choice. |
| `set_winner(winner)` | Sets the `winner` flag (`True` / `False`). |
| `increase_score()` | Adds 1 to the player's `score`. |

### The `RockPaperScissorsGame`

This class has four attributes: `choices`, `user_player`, `computer_player`, and `sets`.

- `choices`: the list of valid choices (`rock`, `paper`, `scissors`).
- `user_player`: a `RockPaperScissorsPlayer` named after the user's input (defaults to `Player` if left empty).
- `computer_player`: a `RockPaperScissorsPlayer` named `Computer`.
- `sets`: the number of sets the user wants to play.

It also has a class constant, `BEATS`, which defines the rules of the game. Each key beats its value:

```python
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
```

And it has seven methods:

#### The `_ask_sets()` method

This static method asks the user for the number of sets and keeps asking until the input is a positive whole number. Inputs like `abc`, `0`, or `-2` are rejected with a message, so the game can never start with an invalid number of sets.

#### The `get_user_choice()` method

Asks the user to enter `rock`, `paper`, or `scissors`. The input is cleaned with `strip().lower()`, so `Rock` and ` paper ` are valid. If the input is invalid, it prints an error and asks again. A valid choice is saved on `user_player` and returned.

#### The `get_computer_choice()` method

Picks a random item from `choices` with `random.choice`, saves it on `computer_player`, and returns it.

#### The `compare_equal(first, second)` method

A tiny helper that returns `True` if both values are equal. It is used to detect ties in a round.

#### The `compare_choices_winner(user_choice, computer_choice)` method

Compares the two choices of a round:

- If they are equal, it returns `None` (a tie, nobody gets a point).
- If the user's choice beats the computer's (checked with `BEATS`), the user's score is increased and a message like `Matin wins! rock beats scissors.` is returned.
- Otherwise, the computer's score is increased and a message like `Computer wins! rock beats scissors.` is returned.

#### The `choose_winner()` method

This is the main loop of the game. It keeps a counter called `sets_played` and repeats until it reaches `sets`:

1. Get the user's choice and the computer's choice.
2. Print the computer's choice.
3. Call `compare_choices_winner` **once**, because it also updates the scores.
4. On a tie, print a message and replay the round (the set is not counted).
5. Otherwise, print the result and increase `sets_played`.

#### The `game()` method

Runs `choose_winner()` and then compares the final scores:

- Higher user score: the user is marked as the winner (`set_winner(True)`) and a winning message is returned.
- Higher computer score: the computer is marked as the winner and a winning message is returned.
- Equal scores: a tie message is returned.

## Game Flow

```
start
  -> ask name and number of sets
  -> repeat until all sets are played:
       user choice + computer choice
       tie?  -> replay (not counted)
       else  -> update score, print result, count the set
  -> compare final scores and print the final result
```

## Project Structure

```
.
├── src/
│   └── rock_paper_scissors.py
└── README.md
```
