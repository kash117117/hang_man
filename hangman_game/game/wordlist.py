import random

WORD_CATEGORIES = {
    "Animals": ["elephant", "giraffe", "kangaroo", "dolphin", "penguin",
                "tiger", "lion", "alligator", "zebra", "cheetah"],
    "Countries": ["canada", "brazil", "japan", "germany", "india",
                  "france", "egypt", "mexico", "china", "italy"],
    "Programming": ["python", "javascript", "java", "csharp", "ruby",
                    "html", "css", "typescript", "sql", "swift"],
    "Science": ["physics", "chemistry", "biology", "astronomy", "geology",
                "thermodynamics", "optics", "genetics", "ecology", "nanotechnology"]
}


def choose_category():
    categories = list(WORD_CATEGORIES.keys())
    print("\n=== Welcome to Hangman ===")
    print("please choose a category:")
    for i, cat in enumerate(categories, start=1):
        print(f"{i}. {cat}")

    while True:
        choice = input("Enter the number of the category: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]
        print("Invalid choice. Please try again.")


def get_random_word(category=None):
    if category is None:
        category = random.choice(list(WORD_CATEGORIES.keys()))
    word = random.choice(WORD_CATEGORIES[category])
    return category, word
