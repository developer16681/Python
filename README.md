# Python Projects & Practice Repository

A curated collection of Python scripts, categorized by application domain: games & 3D simulations, data science & machine learning examples, foundational language exercises, and supporting multimedia assets.

---

## 📂 Project Structure

```
.
├── audio/            # Sound effects (.wav) and background music assets
├── basics/           # Python fundamental concepts and syntax practice
├── data_science/     # NumPy, Pandas, Matplotlib, and Machine Learning algorithms
├── games/            # 2D and 3D games and physics simulations (Ursina, Pygame)
└── text_files/       # Sample text data files
```

---

## 📁 Directory Overview

### 🎮 [`games/`](./games)
Interactive games, 2D arcade classics, and progressive 3D prototype versions:
- **3D Progressive Builds (`3d_1.0.py` – `3d_1.9.py`, `Fixed Script (3d_1.3).py`)**: 3D prototype iterations powered by the [Ursina](https://www.ursinaspaces.org/) engine, featuring first-person controls, procedural sound synthesis, coin collection, and multiple weapon types.
- **`space_fighter.py`**: 3D space shooter simulation with procedurally synthesized audio, laser projectile mechanics, particle explosions, and enemy wave spawning.
- **Pac-Man Implementations**:
  - `pacman.py`: Classic arcade maze navigation and ghost logic.
  - `Pacman_Gemini.py`: Pygame-based Pac-Man implementation with sound effects and animations.
  - `pacman_Github_copilot.py`: Clean maze navigation variant.
- **`mario.py`**: Retro 2D platformer with running, jumping physics, platforms, collectibles, and enemy collision.
- **`Snake_Game.py`**: Grid-based classic Snake arcade game built with Pygame.
- **`neon_shift_main.py`**: Fast-paced synthwave-themed obstacle runner with audio effects.
- **`particles.py`**: Interactive 2D physics particle fountain responding to real-time mouse inputs.
- **`newcopilotgame.py`**: 2D arcade game experiment.

### 📊 [`data_science/`](./data_science)
Data manipulation, numerical computation, visualization, and ML implementations:
- **NumPy & Arrays**:
  - `Creating a Numpy Array.py`, `Data Types in Numpy.py`, `Basic Array Operations.py`, `Math Operations on DataType Array.py`, `Accessing the Array Index.py`, `printing_array.py`
- **Pandas & DataFrames**:
  - `Creating a Series using a List.py`, `Creating a DataFrame using a Dictionary.py`, `pdpd.py` (DataFrame exploration with `head()`, `tail()`, and `info()`), `Reading CSV and JSON Files.py`
- **Machine Learning**:
  - `KMeans Algorithm.py`: Unsupervised clustering example using scikit-learn.
  - `Logistic Regression Algorithm.py`: Binary classification model with train/test splitting and accuracy evaluation.
- **Data Visualization & Stats**:
  - `matplot.py`: Line and bar chart creation with Matplotlib.
  - `statistics.py`: Calculations with Python's built-in `statistics` module (mean, median, mode, stdev).

### 🐍 [`basics/`](./basics)
Core Python language fundamentals and standard library demonstrations:
- **`def.py`**: Function declarations, parameter passing, and return values.
- **`list.py` & `tuple.py`**: Sequence data structures, indexing, slicing, and methods.
- **`math.py`**: Trigonometric, logarithmic, and power functions in the `math` module.
- **`random_demo.py`**: Random numbers, shuffling, and sampling with the `random` module.
- **`time.py`**: Epoch timestamps, delays (`sleep`), and execution timing.
- **`prime.py`**: Prime number checker and generator logic.
- **`file.py`**: Basic text file reading and handling.
- **`print.py` & `new22.py`**: Output formatting and basic variable assignments.

### 🔊 [`audio/`](./audio)
Sound effects and background music in uncompressed 16-bit PCM WAV format used across the games:
- **Background Music**: `bgm.wav`, `bg_music.wav`
- **Sound Effects**: `coin.wav`, `explosion_snd.wav`, `hit_snd.wav`, `jump.wav`, `laser_snd.wav`, `reload.wav`, `shoot.wav`, `shoot_pistol.wav`, `shoot_shotgun.wav`, `shoot_smg.wav`, `switch.wav`

### 📄 [`text_files/`](./text_files)
- **`days.txt`**: Sample plaintext line data for string and iteration exercises.
- **`data.txt`**: Sample multi-line text used for file I/O operations (`open`, `read`, `write`).
- **`people.csv`**: Sample tabular dataset with demographic records for Pandas CSV parsing exercises.

---

## 🚀 Getting Started

### Prerequisites & Installation

Python 3.9+ is recommended. Install all repository dependencies via `requirements.txt`:

```bash
pip install -r requirements.txt
```


### Running Scripts

Execute scripts directly with Python:

```bash
# Run a game
python games/Snake_Game.py
python games/space_fighter.py

# Run a data science script
python "data_science/Logistic Regression Algorithm.py"

# Run a basics exercise
python basics/prime.py
```
