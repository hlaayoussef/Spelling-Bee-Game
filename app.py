import streamlit as st
import random
from gtts import gTTS  # For text-to-speech (optional)
import os

# Word database (word : hint)
WORD_DB = {
    "easy": {
        "cat": "A furry pet that meows.",
        "dog": "A loyal animal that barks.",
        "sun": "It gives us light during the day.",
        "pen": "You use it to write on paper.",
        "hat": "You wear it on your head.",
    },
    "medium": {
        "apple": "A red or green fruit.",
        "tiger": "A big striped cat.",
        "happy": "The opposite of sad.",
        "water": "You drink it to stay hydrated.",
        "house": "A place where people live.",
    },
    "hard": {
        "elephant": "A giant animal with a trunk.",
        "giraffe": "A tall animal with a long neck.",
        "rainbow": "Appears in the sky after rain.",
        "dinosaur": "Prehistoric reptile.",
        "butterfly": "An insect with colorful wings.",
    }
}

def scramble_word(word):
    """Returns a scrambled version of the word."""
    letters = list(word)
    random.shuffle(letters)
    return ''.join(letters)

def text_to_speech(text, filename="word.mp3"):
    """Converts text to speech (optional)."""
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

def main():
    st.title("🎯 Word Scramble Game")
    st.write("Unscramble the letters to form the correct word!")

    # Difficulty selection
    difficulty = st.selectbox(
        "Choose difficulty:",
        ["easy", "medium", "hard"]
    )

    # Initialize session state
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_word' not in st.session_state:
        st.session_state.current_word = random.choice(list(WORD_DB[difficulty].keys()))
    if 'scrambled_word' not in st.session_state:
        st.session_state.scrambled_word = scramble_word(st.session_state.current_word)

    # Display scrambled word & hint
    st.subheader(f"Scrambled Word: **{st.session_state.scrambled_word}**")
    st.write(f"💡 Hint: {WORD_DB[difficulty][st.session_state.current_word]}")

    # User input
    user_guess = st.text_input("Your guess:").strip().lower()

    # Check answer
    if st.button("Submit"):
        if user_guess == st.session_state.current_word:
            st.success("✅ Correct! Well done!")
            st.session_state.score += 1
            st.balloons()
            
            # Play pronunciation (optional)
            if st.checkbox("🔊 Play pronunciation"):
                audio_file = text_to_speech(st.session_state.current_word)
                st.audio(audio_file, format="audio/mp3")
                os.remove(audio_file)  # Clean up
            
            # Load new word
            st.session_state.current_word = random.choice(list(WORD_DB[difficulty].keys()))
            st.session_state.scrambled_word = scramble_word(st.session_state.current_word)
            st.experimental_rerun()  # Refresh for new word
        else:
            st.error("❌ Incorrect! Try again.")

    # Display score
    st.write(f"🏆 Score: {st.session_state.score}")

if __name__ == "__main__":
    main()
