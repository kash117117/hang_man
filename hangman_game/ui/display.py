from game.ascii_art import HANGMAN_STAGES

def show_welcome(game_state):
    print("You can guess single letters, multiple letters, or the full word!")
    print(f"Category: {game_state['category']}")
    print("Good luck!\n")


def update_display(game_state):
    word = game_state["word"]
    correct = game_state["correct_letters"]
    guessed = game_state["guessed_letters"]
    attempts = game_state["attempts"]
    max_attempts = game_state["max_attempts"]

    # Show current hangman ASCII stage
    print("\n" + HANGMAN_STAGES[attempts])

    # Display the word with guessed letters revealed
    display_word = [letter if letter in correct else "_" for letter in word]
    print(f"New word selected from: {game_state['category']}")
    print("Word:", " ".join(display_word))

    # Display guessed letters
    all_guessed = sorted(correct | guessed)
    print(f"Guessed letters: {' '.join(all_guessed) if all_guessed else 'None'}")

    # Display remaining attempts
    remaining = max_attempts - attempts
    print(f"Remaining attempts: {remaining} ({remaining} → 0)")


def get_guess():
    return input("\nEnter your guess (single letter, multiple letters, or full word): ").strip()


def end_game(game_state):
    word = game_state["word"]
    correct = game_state["correct_letters"]
    attempts = game_state["attempts"]

    print("\n" + HANGMAN_STAGES[attempts])

    if all(letter in correct for letter in word):
        print(f"\n🎉 Congratulations! You guessed the word: {word.upper()}")
    else:
        print(f"\n💀 Game Over! The word was: {word.upper()}")
