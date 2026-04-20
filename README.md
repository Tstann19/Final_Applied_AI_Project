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

Difficulty Easy:
- Example 1:
    - Secret Pokemon: Piplup (Water)
    - Input: Pikachu 
    - Output: Its blue hue is instantly recognizable, a vibrant, calming color.

Difficulty Normal:
- Example 2:
    - Secret Pokemon: Gardevoir (Fairy, Psychic)
    - Input: Vulpix
    - Output: It carries a weight of knowing, a burden of foresight’s grace.

Difficulty Hard:
- Example 3:
    - Secret Pokemon: Mew (Psychic)
    - Input: Bulbasaur                 
    - Output: A whisper of dawn, cradled in amethyst skies,

Used all guesses:
- Output: No guesses left! The secret Pokemon was Sneasel (#215).

Won the guesser:
- Output: Correct! The secret Pokemon was Muk

# Design Decisions 

- I built the application this way because it made more sense to fetch the data then create multiple hints to assist the player as the game went on. I felt that the user should be given hints even if the user got it wrong to assist them this way. I also had the guardrail in place so the hints don't lead the player astray from the secret pokemon.

- Some trade-offs I made were having more simplistic type hints because of the type of AI version I'm using, and a working application. Many of the hints are a bit more cryptic in general across all difficulties due to the AI (Gemini Gemma-3-1b-it) than I'd prefer for the user. However, this model was one that was able to work in my application so I decided to keep it.
I also made some UI changes to make the UI more cohesive but slighty more displeasing in look for the game to look very similar to the other game (number guesser). 

# Testing Summary 

What Worked:
- I was able to test name matching, and generating proper hints. The AI agent was able to work how it should in generating hints for the user to take into account. Name matching was also important so the user could guess the pokemon without worrying about senstivity and whitespace.

What Didn't:
- I'd say the one that kinda didn't work as well was the guardrails using the AI. That was kinda difficult to implement.

What I Learned:
- I learned how to make a tester on an AI agent and it's own validation. 
- Also how to apply an AI agent directly onto logic to produce a working game.

# Reflection 

- This project taught me how to utilize my own agent within my own unique project. That creating an application with an AI agent requires validation while working with it primarily. As I've spent a good chunk of time making sure the validation in hints was somewhat viable/helpful. I also learned how to document accordingly. I used this README and my own google doc to keep track of my general ideas along with making sure my project meets designated requirements. In times, I needed more help using Claude and Gemini helped me advance in my own work promply. I realized a good prompt goes a very long way. Otherwise, this project has been helpful in adding a new feature to an already working application.

# Loom video Link

https://github.com/user-attachments/assets/6f994379-00b6-4c5e-b68b-010c7ed2ac21



