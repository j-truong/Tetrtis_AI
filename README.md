# Tetris AI
Developed an AI to learn to play the game Tetris utlising the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. Trialled many heuristics and input data, but have not achieved a perfect input heuristic for the AI to learn to play the game effectively. 

Games are ran synchronously such that when the current spectated game has terminated, the next game that remains alive will be spectated. This continues the whole population in that generation has terminated. Termination is when the tetrimonoes (game pieces) has stacked greater than the maximum capacity of the game board.

This project is still under progress.

![Alt Text](https://github.com/j-truong/Tetrtis_AI/blob/master/images/tetris_gif1.gif)

## Prerequisites

```
pip install requirements.txt
```

## Script
Train model
```
python main.py
```
