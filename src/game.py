"""
A command-line Rock Paper Scissors game.

The module provides two classes: :class:`RockPaperScissorsPlayer`, which holds
the state of a single player, and :class:`RockPaperScissorsGame`, which runs
a multi-set match between the user and the computer.
"""

import random
from typing import Optional


class RockPaperScissorsPlayer:
    """
    Represents a player in a Rock Paper Scissors game.

    :ivar name: The display name of the player.
    :vartype name: str
    :ivar choice: The player's most recent choice, or ``None`` if the player
        has not chosen yet.
    :vartype choice: str or None
    :ivar winner: ``True`` if the player has won the game, otherwise ``False``.
    :vartype winner: bool
    :ivar score: The number of sets the player has won.
    :vartype score: int
    """

    def __init__(self, name: str = "Computer"):
        """
        Initialize a new player.

        :param name: The display name of the player.
        :type name: str
        """

        self.name: str = name
        self.choice: str = None
        self.winner: bool = False
        self.score: int = 0

    def make_choice(self, choice: str):
        """
        Set the player's current choice.

        :param choice: The choice to store (``"rock"``, ``"paper"`` or
            ``"scissors"``).
        :type choice: str
        :return: None
        :rtype: None
        """

        self.choice: str = choice

    def set_winner(self, winner: bool):
        """
        Set the player's winner status.

        :param winner: ``True`` if the player won the game, otherwise ``False``.
        :type winner: bool
        :return: None
        :rtype: None
        """

        self.winner: bool = winner

    def increase_score(self):
        """
        Increase the player's score by 1.

        :return: None
        :rtype: None
        """

        self.score += 1


class RockPaperScissorsGame:
    """
    Represents a Rock Paper Scissors game between a user and the computer.

    On creation the game asks the user for a name and for the number of sets
    to play. Tied rounds do not count as a set and are replayed.

    :cvar BEATS: Mapping from each choice to the choice it defeats.
    :vartype BEATS: dict[str, str]
    :ivar choices: The valid choices a player may make.
    :vartype choices: list[str]
    :ivar user_player: The human player.
    :vartype user_player: RockPaperScissorsPlayer
    :ivar computer_player: The computer-controlled player.
    :vartype computer_player: RockPaperScissorsPlayer
    :ivar sets: The number of decisive sets to be played.
    :vartype sets: int
    """

    BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

    def __init__(self):
        """
        Initialize the game by prompting the user for input.

        Prompts for the user's name (defaults to ``"Player"`` if left empty)
        and for the number of sets to play.
        """

        self.choices: list[str] = list(self.BEATS)
        name: str = input("Enter your name: ").strip() or "Player"
        self.user_player: RockPaperScissorsPlayer = RockPaperScissorsPlayer(name=name)
        self.computer_player: RockPaperScissorsPlayer = RockPaperScissorsPlayer(name="Computer")
        self.sets: int = self._ask_sets()

    @staticmethod
    def _ask_sets() -> int:
        """
        Prompt the user for the number of sets until a valid value is entered.

        The prompt repeats until the input is a positive whole number.

        :return: The number of sets to play (always greater than zero).
        :rtype: int
        """

        while True:
            raw: str = input("Enter the number of sets you want to play: ").strip()

            if raw.isdigit() and int(raw) > 0:
                return int(raw)

            print("Please enter a positive whole number.")

    def get_user_choice(self) -> str:
        """
        Prompt the user for a choice until a valid one is entered.

        The input is stripped and lower-cased before validation. The valid
        choice is also stored on :attr:`user_player`.

        :return: The user's choice (``"rock"``, ``"paper"`` or ``"scissors"``).
        :rtype: str
        """

        while True:
            user_choice: str = input(f"Enter your choice ({', '.join(self.choices)}): ").strip().lower()

            if user_choice in self.choices:
                self.user_player.make_choice(user_choice)

                return user_choice

            print(f"Invalid choice. Please try again. You must choose from {', '.join(self.choices)}.")

    def get_computer_choice(self) -> str:
        """
        Pick a random choice for the computer.

        The choice is also stored on :attr:`computer_player`.

        :return: The computer's choice (``"rock"``, ``"paper"`` or
            ``"scissors"``).
        :rtype: str
        """

        self.computer_player.make_choice(random.choice(self.choices))

        return self.computer_player.choice

    def compare_equal(self, first: str, second: str) -> bool:
        """
        Check whether two values are equal.

        :param first: The first value to compare.
        :type first: str
        :param second: The second value to compare.
        :type second: str
        :return: ``True`` if both values are equal, otherwise ``False``.
        :rtype: bool
        """

        return first == second

    def compare_choices_winner(self, user_choice: str, computer_choice: str) -> Optional[str]:
        """
        Determine the winner of a single round and update the scores.

        The winning player's score is increased by 1. Nothing is changed when
        the round is a tie.

        :param user_choice: The user's choice.
        :type user_choice: str
        :param computer_choice: The computer's choice.
        :type computer_choice: str
        :return: A message announcing the round winner, or ``None`` if the
            round is a tie.
        :rtype: str or None
        """

        if self.compare_equal(user_choice, computer_choice):
            return None

        if self.BEATS[user_choice] == computer_choice:
            self.user_player.increase_score()

            return f"{self.user_player.name} wins! {user_choice} beats {computer_choice}."

        self.computer_player.increase_score()

        return f"{self.computer_player.name} wins! {computer_choice} beats {user_choice}."

    def choose_winner(self) -> None:
        """
        Play the requested number of sets.

        Each round collects both players' choices, prints the outcome and
        updates the scores. Tied rounds do not count as a set and are replayed.

        :return: None
        :rtype: None
        """

        sets_played: int = 0

        while sets_played < self.sets:
            user: str = self.get_user_choice()
            computer: str = self.get_computer_choice()

            print(f"Computer chose {computer}.")

            result: Optional[str] = self.compare_choices_winner(user, computer)

            if result is None:
                print(f"It's a tie! Both players chose {user}. Please play again.")

                continue

            print(result)

            sets_played += 1

    def game(self) -> str:
        """
        Play the whole game and report the final result.

        Runs :meth:`choose_winner`, compares the final scores, and marks the
        overall winner (if any) via :meth:`RockPaperScissorsPlayer.set_winner`.

        :return: A message describing the overall winner and the final score,
            or announcing a tie.
        :rtype: str
        """

        self.choose_winner()

        user_score: int = self.user_player.score
        computer_score: int = self.computer_player.score

        if user_score > computer_score:
            self.user_player.set_winner(True)

            return f"{self.user_player.name} wins the game with a score of {user_score} to {computer_score}!"
        if user_score < computer_score:
            self.computer_player.set_winner(True)

            return f"{self.computer_player.name} wins the game with a score of {computer_score} to {user_score}!"

        return f"The game is a tie with a score of {user_score} to {computer_score}!"


if __name__ == "__main__":
    while True:
        print("==Rock Paper Scissors Game==")
        print("1. Play")
        print("2. Exit")

        choice: str = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            rps_game: RockPaperScissorsGame = RockPaperScissorsGame()

            print(rps_game.game())
        elif choice == "2":
            print("Exiting the game. Goodbye!")

            break   