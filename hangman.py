import random
import os

words = {
    "programming": {
        "python": "A popular programming language.",
        "programming": "The process of creating software.",
        "developer": "A person who writes code."
    },
    "technology": {
        "computer": "An electronic device for storing and processing data.",
        "internet": "A global computer network.",
        "smartphone": "A mobile device with computing capabilities."
    },
    "games": {
        "hangman": "A classic word guessing game.",
        "chess": "A strategy board game.",
        "ludo": "A board game in which players race their tokens based on dice rolls."
    }
}

def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            return int(file.read())
    else:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

def select_word(category):
    word = random.choice(list(words[category].keys()))
    hint = words[category][word]
    return word, hint

def initialize_game(word):
    hidden_word = ["_"] * len(word)
    return {
        "word": word,
        "hidden_word": hidden_word,
        "guessed_letters": set(),
        "incorrect_guesses": set(),
        "attempts_left": 6,
        "score": 0
    }

def process_guess(game_state, guess):
    word = game_state["word"]
    hidden_word = game_state["hidden_word"]
    guessed_letters = game_state["guessed_letters"]
    incorrect_guesses = game_state["incorrect_guesses"]

    if guess in guessed_letters or guess in incorrect_guesses:
        return game_state, "You already guessed that letter!"
    
    guessed_letters.add(guess)
    
    if guess in word:
        for i in range(len(word)):
            if word[i] == guess:
                hidden_word[i] = guess
        return game_state, "Correct guess!"
    
    game_state["attempts_left"] -= 1
    incorrect_guesses.add(guess)
    return game_state, "Wrong guess!"

def play_hangman():
    print("Welcome to the Word Guessing Game!")
    
    name = input("Enter your name: ")
    city = input("Enter your city: ")
    level = input("Enter your level (beginner/intermediate/advanced): ")
    
    print(f"Hello {name} from {city}, level {level}! Let's play!")

    print("\nAvailable categories: Programming, Technology, Games")
    category = input("Which kind of word do you want to guess? ").lower()
    
    if category not in words:
        print("Invalid category. Defaulting to Programming.")
        category = "programming"
    
    high_score = load_high_score()
    print(f"Current high score: {high_score}")

    total_score = 0
    while True:
        word, hint = select_word(category)
        game_state = initialize_game(word)

        print(f"Hint: {hint}")
        
        while game_state["attempts_left"] > 0:
            print(" ".join(game_state["hidden_word"]))
            print(f"Attempts left: {game_state['attempts_left']}")
            
            guess = input("Guess a letter: ").lower()
            
            while guess in game_state["guessed_letters"] or guess in game_state["incorrect_guesses"]:
                print("You already guessed that letter! Try a different one.")
                guess = input("Guess a letter: ").lower()

            game_state, message = process_guess(game_state, guess)
            print(message)

            if "_" not in game_state["hidden_word"]:
                print(f"Congratulations, {name}! You won this round!")
                game_state["score"] = 6 - game_state["attempts_left"]
                total_score += game_state["score"]
                print(f"Your score this round: {game_state['score']} attempts.")
                break  
        
        if game_state["attempts_left"] == 0:
            print(f"Game over! The word was {game_state['word']}.")
            print(f"Your total score so far: {total_score} attempts.")
        
        if total_score > high_score:
            print(f"New high score! Congratulations!")
            save_high_score(total_score)
            high_score = total_score
        
        continue_game = input("Do you want to play another round? (yes/no): ").lower()
        if continue_game != "yes":
            print(f"Thank you for playing! Your final score is {total_score} attempts.")
            break

play_hangman()