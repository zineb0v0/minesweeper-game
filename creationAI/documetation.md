## The Core Class: `MinesweeperAgentWeb`

This class is the heart of the Minesweeper AI agent. It is responsible for:

- Interacting with the game (clicking tiles, resetting the game, etc.)
- Detecting the game state (which tiles are open, which are mines, etc.)
- Deciding which actions to take using a trained reinforcement learning model.

---

## Constructor: `__init__(self, model)`

When an instance of the `MinesweeperAgentWeb` class is created, the constructor initializes the AI agent and sets up the configurations required to interact with the game.

- **model**: This is the reinforcement learning model that the AI agent uses to decide the best moves. It’s pre-trained on how to play Minesweeper, learning from previous game experiences.

### Initialization Tasks:
- The game window is focused.
- The game is reset (presses the 'F2' key).
- The AI retrieves information about the game mode (beginner, intermediate, expert), and the board's location and dimensions.
- The board state is initialized to start making decisions.

---

## Method: `reset(self)`

This method resets the Minesweeper game by simulating the pressing of the **F2** key. The agent needs to reset the game before starting a new round so that it can make fresh decisions based on the initial state of the game.

---

## Method: `get_loc(self)`

This method detects where the Minesweeper game is located on the screen and identifies the current mode (beginner, intermediate, or expert). The method uses image recognition to find the game board on the screen using images stored in the `pics` directory.

It returns:
- **mode**: The current difficulty level (e.g., beginner, expert).
- **loc**: The coordinates of the game board on the screen.
- **dims**: The dimensions of the game board, such as the number of rows and columns.

---

## Method: `get_tiles(self, tile, bbox)`

This method searches for tiles of a given type within a specified area of the screen (defined by `bbox`).

- **tile**: A specific tile type (e.g., 'unsolved', 'zero', 'one', etc.).
- **bbox**: The area of the screen (bounding box) in which to search for these tiles.

It uses confidence values to accurately locate these tiles. For example, it will search for "zero" tiles (which have no mines around them) or "unsolved" tiles (which haven't been clicked yet).

---

## Method: `get_board(self, bbox)`

This method scans the entire Minesweeper board and returns the current state. It uses image recognition to extract information about each tile (whether it’s a mine, empty, or a number).

It returns a list of tiles where each tile contains:
- Coordinates (location on the board)
- Value (e.g., 'unsolved', 'zero', 'one', etc.)

---

## Method: `get_state(self, board)`

The `get_state` method converts the visual representation of the board into a numerical format that can be used as input for the reinforcement learning model.

- **board**: The list of tiles (from the `get_board` method).

It returns a **NumPy array**, which is the format needed for input into the Deep Q-Network (DQN) model.

---

## Method: `get_action(self, state)`

This method determines the best action to take based on the current state of the game. It uses an **epsilon-greedy strategy** to balance exploration and exploitation.

- **state**: The current game state (in numerical format).

It returns the **index** of the tile to click. The AI will decide which tile it should click based on the state of the board.

---

## Method: `get_neighbors(self, action_index)`

This method identifies the neighboring tiles of a given action. It is useful for understanding the context of the tile before deciding what to do next.

- **action_index**: The index of the tile the agent is considering to click.

It returns a list of neighboring tile values (e.g., values of adjacent tiles).

---

## Method: `step(self, action_index)`

This method is used to perform a move in the game. It simulates the agent clicking on a tile (using the `pyautogui` library) and updates the game state.

- **action_index**: The index of the tile to click.

It returns:
- **state**: The updated state of the board after the move.
- **done**: A boolean indicating if the game has finished (i.e., if the agent has won or lost).

---

## Configuration: Tile Confidence and Mapping

The game uses image recognition to detect the state of the board. To do this, confidence values are assigned to different tile types (e.g., unsolved, zero, one, etc.). These values help the agent identify which tiles are which, with higher confidence values indicating higher accuracy.

- **CONFIDENCES**: A dictionary that maps each tile type (e.g., 'unsolved', 'zero', 'one') to a confidence value used in image recognition.
- **TILES** and **TILES2**: Dictionaries that map tile labels (like 'U', '0', '1') to the corresponding Minesweeper state.

---

## Conclusion

This Minesweeper AI agent is built using **Reinforcement Learning** and **image recognition**. It detects the game board’s state, processes the information, and chooses the best action (which tile to click) based on a trained model. The agent interacts with the game through the `pyautogui` library to click tiles and reset the game.
