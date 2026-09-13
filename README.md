# 🐍 Snake Game

A classic Snake game built with **Python** and **Pygame** — my first project on GitHub!

## Features
- Smooth grid-based movement
- Score and high score tracking
- Increasing difficulty (speeds up as you eat more food)
- Pause / resume (`P`)
- Restart after Game Over (`R`)
- Wall and self-collision detection

## Controls
| Key | Action |
|---|---|
| Arrow Keys / WASD | Move the snake |
| P | Pause / Resume |
| R | Restart (after Game Over) |
| Q / ESC | Quit |

## Requirements
- Python 3.8+
- Pygame

## Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/snake-game.git
cd snake-game

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the game
python snake_game.py
```

## How to Upload This Project to GitHub

1. Create a new repository on GitHub (e.g. `snake-game`) — don't initialize it with a README.
2. In this project folder, run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Snake game"
   git branch -M main
   git remote add origin https://github.com/<your-username>/snake-game.git
   git push -u origin main
   ```
3. Refresh your GitHub page — your project is live! 🎉

## Project Structure
```
snake-game/
├── snake_game.py     # Main game code
├── requirements.txt  # Dependencies
└── README.md         # Project documentation
```

## Possible Improvements (great for a v2!)
- Add sound effects
- Add a start menu
- Save high score to a file
- Add different difficulty levels
- Add obstacles

## License
Feel free to use this project for learning purposes.
