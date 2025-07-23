import streamlit as st
import random
import google.generativeai as genai

# Configure Gemini API key (replace with your actual key)
GEMINI_API_KEY = "AIzaSyAsut5nuxR7w-LrfqhMePB3Q26n3jmtixc"  # Insert your Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Custom CSS for a vibrant, game-like UI
st.markdown("""
    <style>
    .main {
        background-color: #ecd6c0;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput input {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 5px;
    }
    h1 {
        color: #2e7d32;
        font-family: 'Verdana', sans-serif;
        text-align: center;
    }
    h2, h3 {
        color: #388e3c;
        font-family: 'Verdana', sans-serif;
    }
    .stMarkdown {
        font-family: 'Arial', sans-serif;
        color: #333333;
    }
    .success-box {
        background-color: #c8e6c9;
        padding: 10px;
        border-radius: 5px;
        color: #2e7d32;
    }
    .error-box {
        background-color: #ffcdd2;
        padding: 10px;
        border-radius: 5px;
        color: #c62828;
    }
    .roast-box {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        color: #856404;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# Hangman ASCII art for different stages
HANGMAN_STAGES = [
    r"""
     ------
     |    |
          |
          |
          |
          |
    =========
    """,
    r"""
     ------
     |    |
     O    |
          |
          |
          |
    =========
    """,
    r"""
     ------
     |    |
     O    |
     |    |
          |
          |
    =========
    """,
    r"""
     ------
     |    |
     O    |
    /|    |
          |
          |
    =========
    """,
    r"""
     ------
     |    |
     O    |
    /|\   |
          |
          |
    =========
    """,
    r"""
     ------
     |    |
     O    |
    /|\   |
    /     |
          |
    =========
    """,
    r"""
     ------
     |    |
     O    |
    /|\   |
    / \   |
          |
    =========
    """
]

# Function to fetch a random word from Gemini API based on category
def get_random_word(category):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Generate a single random word in the category '{category}' suitable for a Hangman game. The word should be 4-10 letters long, common, and appropriate for all ages. Return only the word in uppercase."
    try:
        response = model.generate_content(prompt)
        word = response.text.strip().upper()
        if 4 <= len(word) <= 10 and word.isalpha():
            return word
        else:
            # Fallback words if API response is invalid
            fallback_words = {
                "Animals": ["ELEPHANT", "GIRAFFE", "KANGAROO", "PENGUIN"],
                "Movies": ["AVATAR", "TITANIC", "JUMANJI", "FROZEN"],
                "Countries": ["BRAZIL", "CANADA", "JAPAN", "ITALY"],
                "Fruits": ["APPLE", "BANANA", "MANGO", "ORANGE"]
            }
            return random.choice(fallback_words[category])
    except Exception as e:
        st.error(f"Error fetching word from Gemini API: {e}")
        # Fallback to a random word from the category
        fallback_words = {
            "Animals": ["ELEPHANT", "GIRAFFE", "KANGAROO", "PENGUIN"],
            "Movies": ["AVATAR", "TITANIC", "JUMANJI", "FROZEN"],
            "Countries": ["BRAZIL", "CANADA", "JAPAN", "ITALY"],
            "Fruits": ["APPLE", "BANANA", "MANGO", "ORANGE"]
        }
        return random.choice(fallback_words[category])

# Function to generate a roast for a wrong guess
def get_roast(guessed_letter):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Generate a short, playful, and family-friendly roast for someone who guessed the letter '{guessed_letter}' incorrectly in a Hangman game. Keep it fun, light-hearted, and under 20 words."
    try:
        response = model.generate_content(prompt)
        roast = response.text.strip()
        if roast:
            return roast
        else:
            # Fallback roasts
            fallback_roasts = [
                f"Oof, {guessed_letter}? Did you pick that letter out of a hat?",
                f"{guessed_letter}? Are you trying to make the hangman laugh?",
                f"Yikes, {guessed_letter} is nowhere close! Are you guessing with your eyes closed?",
                f"{guessed_letter}? Even the word is embarrassed for you!"
            ]
            return random.choice(fallback_roasts)
    except Exception as e:
        st.error(f"Error fetching roast from Gemini API: {e}")
        # Fallback roasts
        fallback_roasts = [
            f"Oof, {guessed_letter}? Did you pick that letter out of a hat?",
            f"{guessed_letter}? Are you trying to make the hangman laugh?",
            f"Yikes, {guessed_letter} is nowhere close! Are you guessing with your eyes closed?",
            f"{guessed_letter}? Even the word is embarrassed for you!"
        ]
        return random.choice(fallback_roasts)

# Initialize session state
def initialize_session_state():
    if "game_state" not in st.session_state:
        st.session_state.game_state = {
            "word": "",
            "category": "",
            "guessed_letters": set(),
            "wrong_guesses": 0,
            "max_wrong": len(HANGMAN_STAGES) - 1,
            "game_over": False,
            "won": False
        }

# Reset game
def reset_game():
    st.session_state.game_state = {
        "word": "",
        "category": "",
        "guessed_letters": set(),
        "wrong_guesses": 0,
        "max_wrong": len(HANGMAN_STAGES) - 1,
        "game_over": False,
        "won": False
    }

# Main game function
def main():
    st.title("Hangman Game")
    st.write("Guess the word by entering one letter at a time! Wrong guesses get roasted!")

    initialize_session_state()

    # Category selection
    st.subheader("Select a Category")
    categories = ["Animals", "Movies", "Countries", "Fruits"]
    category = st.selectbox("Choose a category:", categories, key="category_select")

    # Start game button
    if st.button("Start Game"):
        if category:
            st.session_state.game_state["category"] = category
            st.session_state.game_state["word"] = get_random_word(category)
            st.session_state.game_state["guessed_letters"] = set()
            st.session_state.game_state["wrong_guesses"] = 0
            st.session_state.game_state["game_over"] = False
            st.session_state.game_state["won"] = False
            st.success(f"New game started in {category} category!")
        else:
            st.error("Please select a category.")

    # Display game state
    if st.session_state.game_state["word"]:
        word = st.session_state.game_state["word"]
        guessed_letters = st.session_state.game_state["guessed_letters"]
        wrong_guesses = st.session_state.game_state["wrong_guesses"]
        game_over = st.session_state.game_state["game_over"]
        won = st.session_state.game_state["won"]

        # Display hangman
        st.code(HANGMAN_STAGES[wrong_guesses], language="text")

        # Display word progress
        display_word = " ".join(letter if letter in guessed_letters else "_" for letter in word)
        st.markdown(f"**Word**: {display_word}")

        # Display guessed letters
        st.markdown(f"**Guessed Letters**: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")

        # Check win/loss conditions
        if set(word) <= guessed_letters:
            st.session_state.game_state["game_over"] = True
            st.session_state.game_state["won"] = True
            st.markdown('<div class="success-box">Congratulations! You guessed the word!</div>', unsafe_allow_html=True)
        elif wrong_guesses >= st.session_state.game_state["max_wrong"]:
            st.session_state.game_state["game_over"] = True
            st.markdown(f'<div class="error-box">Game Over! The word was: {word}</div>', unsafe_allow_html=True)

        # Letter input
        if not game_over:
            with st.form(key="guess_form"):
                guess = st.text_input("Enter a letter:", max_chars=1).upper()
                submit = st.form_submit_button("Guess")

                if submit and guess:
                    if len(guess) != 1 or not guess.isalpha():
                        st.error("Please enter a single letter.")
                    elif guess in guessed_letters:
                        st.error("You already guessed that letter.")
                    else:
                        st.session_state.game_state["guessed_letters"].add(guess)
                        if guess not in word:
                            st.session_state.game_state["wrong_guesses"] += 1
                            roast = get_roast(guess)
                            st.markdown(f'<div class="error-box">{guess} is not in the word!</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="roast-box">{roast}</div>', unsafe_allow_html=True)
                        else:
                            st.success(f"{guess} is in the word!")

    # Reset button
    if st.button("Reset Game"):
        reset_game()
        st.success("Game has been reset!")

if __name__ == "__main__":
    main()