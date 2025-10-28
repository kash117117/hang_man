from pathlib import Path
from datetime import datetime
from game.wordlist import get_random_word, choose_category
from ui.display import show_welcome, update_display, get_guess, end_game
from game.ascii_art import HANGMAN_STAGES

LOG_ROOT = Path("game_log")


def initialize_game():
    """Initialize a new game state"""
    category = choose_category()
    _, word = get_random_word(category)
    return {
        "category": category,
        "word": word.lower(),
        "correct_letters": set(),
        "guessed_letters": set(),
        "wrong_guesses": [],
        "attempts": 0,
        "max_attempts": len(HANGMAN_STAGES) - 1,
        "game_over": False,
        "progress_trace": [],
        "last_stage_reached": 0
    }


def is_valid_guess(guess):
    """Check if guess is valid: single alphabetic letter or full word."""
    guess = guess.strip().lower()
    return guess.isalpha() and len(guess) > 0


def process_guess(game_state, guess):
    """Process a valid guess (single letter or full word)."""
    word = game_state["word"]
    guess = guess.lower().strip()

    # Quit mid-game
    if guess == "quit":
        game_state["game_over"] = True
        return "quit"

    # Full word guess
    if len(guess) > 1:
        if guess == word:
            game_state["correct_letters"].update(word)
        else:
            game_state["attempts"] += 1
            game_state["wrong_guesses"].append(guess)
        return

    # Single-letter guess
    if len(guess) == 1 and guess.isalpha():
        if guess in game_state["word"]:
            game_state["correct_letters"].add(guess)
        else:
            if guess not in game_state["guessed_letters"]:
                game_state["attempts"] += 1
                game_state["wrong_guesses"].append(guess)

        game_state["guessed_letters"].add(guess)


def check_game_status(game_state):
    """Check if the player has won, lost, or continues."""
    word = game_state["word"]
    correct = game_state["correct_letters"]

    # Save hangman stage progress
    game_state["last_stage_reached"] = game_state["attempts"]

    # Record progress trace
    display_word = "".join([letter if letter in correct else "_" for letter in word])
    game_state["progress_trace"].append(display_word)

    if all(letter in correct for letter in word):
        game_state["game_over"] = True
        return "win"
    elif game_state["attempts"] >= game_state["max_attempts"]:
        game_state["game_over"] = True
        return "lose"
    return "continue"


def calculate_score(word_length, wrong_attempts):
    """Compute round score (example formula from assignment)."""
    return max(0, (word_length * 10) - (wrong_attempts * 5))


def log_game(game_state):
    """Create game log file with session notes."""
    LOG_ROOT.mkdir(exist_ok=True)

    # Determine next game folder number
    existing_games = [p for p in LOG_ROOT.iterdir() if p.is_dir() and p.name.startswith("game")]
    game_numbers = [int(p.name.replace("game", "")) for p in existing_games if p.name[4:].isdigit()]
    next_game_number = max(game_numbers, default=0) + 1
    game_folder = LOG_ROOT / f"game{next_game_number}"
    game_folder.mkdir(exist_ok=True)

    word = game_state["word"]
    correct = game_state["correct_letters"]
    wrong = game_state["wrong_guesses"]
    attempts = game_state["attempts"]
    result = "Win" if all(letter in correct for letter in word) else "Loss"
    score = calculate_score(len(word), attempts)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build progress trace for session notes
    trace_str = " -> ".join(game_state["progress_trace"])
    session_notes = (
        f"\nSession Notes:\n"
        f"- ASCII hangman reached state {game_state['last_stage_reached']} "
        f"after wrong guess '{wrong[-1] if wrong else 'None'}'.\n"
        f"- Progress trace: {trace_str}\n"
        f"{'-' * 40}\n"
    )

    log_text = (
        f"Category: {game_state['category']}\n"
        f"Word: {word}\n"
        f"Guessed letters: {', '.join(sorted(correct | set(wrong)))}\n"
        f"Wrong guesses: {', '.join(wrong) if wrong else 'None'}\n"
        f"Attempts used: {attempts}\n"
        f"Final result: {result}\n"
        f"Score: {score}\n"
        f"Timestamp: {timestamp}\n"
        f"{session_notes}"
    )

    log_file = game_folder / "log.txt"
    log_file.write_text(log_text, encoding="utf-8")


def start_game():
    """Run the full hangman game."""
    game_state = initialize_game()
    show_welcome(game_state)

    while not game_state["game_over"]:
        update_display(game_state)
        guess = get_guess()

        if not is_valid_guess(guess):
            print("❌ Invalid input. Please enter a single alphabetic letter or the full word.")
            continue

        if guess.lower() == "quit":
            print("\n🚪 You quit the game early. Goodbye!")
            game_state["game_over"] = True
            break

        process_guess(game_state, guess)
        status = check_game_status(game_state)

        if status in ("win", "lose"):
            break

    end_game(game_state)
    log_game(game_state)
