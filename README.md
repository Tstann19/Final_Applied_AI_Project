# 🎮 Game Glitch Investigator Original Project Summary

- The original application is a website in which clients would guess the secret number from a designated range (i.e. 1 - 100). The game allows hints to be given to the user to assist in guessing the secret number. There is also the ability to change the game's difficulty to easy, medium, and hard.

# Additional Pokemon Guessing Game

- The additional feature on this application is a pokemon guessing game. Having just a number guesser on the application will eventually become repetitive to potential users, so having an additional game with a bit more difficulty would be entertaining. Especially for those that like to challenge themselves.

- This addition would allow a user to guess the secret pokemon. My application will utilize the PokeAPI to fetch correct information about all the pokemon data available. Difficulty would be decided on how many guesses would be avaliable to the user (12 - easy, 8 - medium, 5 - hard). Hints will be given by the AI Agent that will utilize difficulty-scaled riddles. Hard being the most cryptic and Easy being the most obvious.

# System Diagram Summary

- The system diagram displays how the Pokemon guessing game operates when making the hints for the user. The application first takes the user's input of asking for a hint. Then fetches the data of the secret pokemon to generate LLM Prompting to create a hint. The guardrail validation is a checker to make sure the hint exemplies the specified pokemon data (whether cryptic or obvious). Afterwards the hint is displayed to the user to assist in making their next guess.

# Setup Instructions

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `streamlit run app.py`

# Sample Interactions 

Example 1:
    Input:                  Output:

Example 2:
    Input:                  Output:

Example 3:
    Input:                  Output:

# Design Decisions 

- I built the application this way because ...

- Some trade-offs I made were ...

# Testing Summary 

What Worked:
- 
- 
What Didn't:
- 
- 
What I Learned:
- 
- 

# Reflection 

- What this project taught you about AI and problem-solving?


# Loom video Link of 2-3 examples of the project working.


