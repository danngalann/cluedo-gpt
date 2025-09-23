This repository contains an AI-powered Cluedo-inspired game. In this game, a set of players interact with the AI by asking questions about a crime, and they must deduce the culprit, the weapon and the motive of the crime based on the AI's responses. This differs from the classical Cluedo game by removing the usual cards, introducing a motive, and playing directly against a game master.

A team can be a single individual or a team, and after their solution proposal they will receive a grading of their solution, indicating how many elements they got correct.

## Game flow
1. **Game Initialization**: A game owner will create a game, and will interact with the AI to create an original story with personalized characters, weapons and more.
2. **Game Play**: Players will join the game and interact with the AI to ask questions about the crime. The AI will respond based on the story created during the initialization phase. Because the story is static, and the questions are isolated, we prevent context rot hallucinations. Players will be allowed a set number of questions and proposals.
3. **Solution Proposal**: Players will propose their solution to the crime, and will receive feedback. If more than one proposal is allowed, they can continue asking questions and proposing solutions until they run out of proposals.
4. **Game Conclusion**: The game concludes when all players have exhausted their proposals, or when the owner decides to end the game. The final results will be displayed, showing how many elements each player got correct.