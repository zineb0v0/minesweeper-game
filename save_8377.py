# save_8377.py
import pickle
import os
from DQN_agent import DQNAgent
from MinesweeperEnv import MinesweeperEnv

# 1. Crée les dossiers si absents
os.makedirs("models", exist_ok=True)
os.makedirs("replay", exist_ok=True)

# 2. Sauvegarde
env = MinesweeperEnv(9, 9, 10)
agent = DQNAgent(env, "minesweeper_dqn")

agent.model.save("models/minesweeper_dqn_8377.h5")  # Modèle
with open("replay/minesweeper_dqn_8377.pkl", "wb") as f:
    pickle.dump(agent.replay_memory, f)  # Mémoire d'expérience

print("✅ Sauvegarde réussie dans :")
print(f"- models/minesweeper_dqn_8377.h5")
print(f"- replay/minesweeper_dqn_8377.pkl")