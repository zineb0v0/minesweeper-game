### **MinesweeperAI – AI-Powered Minesweeper Game with Deep Reinforcement Learning**


![image](https://github.com/user-attachments/assets/2ba7bf64-5cb7-439d-8602-abbf251948d6)

Overview
MinesweeperAI is a desktop-based application that combines the classic Minesweeper game with Artificial Intelligence capable of learning to play it autonomously. Developed as part of an academic project, it leverages Deep Q-Learning (DQN) to enable the agent to navigate the grid, avoid mines, and maximize rewards through trial and error. The platform is structured with clear modularity: game engine, AI model, training pipeline, and visual interface — ensuring extensibility and clarity for future improvements.

This project was developed during the 2024/2025 academic year as part of a Computer Science curriculum.

🎯 Features
Classic Minesweeper Gameplay: Enjoy the traditional game with a fully functioning board, flags, and mine logic.

AI-Powered Agent: The AI learns to play Minesweeper via Deep Reinforcement Learning using a Deep Q-Network (DQN).

Training Pipeline: Train the agent with train.py, including replay memory, exploration strategy, and reward shaping.

Visual TensorBoard Metrics: Real-time performance and loss monitoring via TensorBoard.

Sound & UI Feedback: Includes sound effects and visual feedback for win/loss/game progress.

Replay Memory: Saves gameplay experience for training the AI.

🗂 Project Structure
<pre> 
  .
├── DQN
│   ├── DQN.py
│   ├── DQN_agent.py
│   ├── minesweeper_env.py
│   ├── my_tensorboard2.py
│   ├── test.py
│   ├── train.py
│   ├── models
│   ├── replay
│   └── logs
│       └── conv64x4_dense512x2_y0.1_minlr0.001
├── DimineurGame
│   └── logs
│       └── conv64x4_dense512x2_y0.1_minlr0.001
│           ├── events.out.tfevents.1746742238.DESKTOP-2Q5NU70.12844.0.v2
│           └── train
├── creationAI
│   ├── creation.py
│   ├── documetation.md
│   └── pics
├── images
├── logs
├── mines
│   ├── ChampMines.py
│   └── mine.py
├── models
│   └── conv64x4_dense512x2_y0.1_minlr0.001.h5
├── replay
│   └── conv64x4_dense512x2_y0.1_minlr0.001.pkl
├── sounds
│   ├── ai_move.wav
│   ├── defeat.mp3
│   ├── put_flag.wav
│   ├── reveal_move.wav
│   └── victory.wav
├── .gitignore
├── LICENSE
├── README.md
├── ai.py
├── constants.py
├── grille.py
├── main.py
├── minesweeper.log
├── my_tensorboard.py

</pre>

🧠 How the AI Works
The AI agent uses a Deep Q-Network (DQN) with an ε-greedy policy. It interacts with the environment (grid), receives rewards for safe moves, and penalties for hitting mines. The Q-values are learned through backpropagation based on the agent’s experience.

Core Concepts:

States: Representation of the current grid.

Actions: Choose a cell to click.

Rewards: +10 for safe click, -50 for mine, +100 for win.

Neural Network: Fully connected layers to approximate Q-values.

Replay Buffer: Store past moves for batch training.

🚀 Getting Started
Prerequisites
Python 3.8+
pip
TensorFlow / Keras
pygame

NumPy

TensorBoard

Install dependencies:

pip install -r requirements.txt

🛠️ Future Improvements

Integrate convolutional neural networks for spatial learning.

Implement curriculum learning to train on smaller grids first.

Web-based UI using Flask or PyScript.

Save and load training checkpoints.
