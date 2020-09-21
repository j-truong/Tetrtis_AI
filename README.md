# Tetris AI
Developed an AI to learn to play the game Tetris utlising the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. Trialled many heuristics and input data, but have not achieved a perfect input heuristic for the AI to learn to play the game effectively. 

All games are ran synchronously until a game has terminated; in this case is when the game has stacked over the maximum capacity of the board. After the current spectated game has terminated, the next remaining alive game will be displayed until the entire population has been terminated in that generation.

By default, the population size is 200 and number of genomes is 100, but these parameters can be altered.

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
