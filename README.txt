# Othello (Reversi) – CSE 4301 Project

A Python/Pygame implementation of the classic **Othello (Reversi)** board game created for **CSE 4301: Introduction to Artificial Intelligence**.

This project supports both **human vs. human** and **human vs. AI** gameplay. The AI opponent uses the **minimax algorithm with alpha-beta pruning** to make efficient and strategic moves.

---

## Preview

<!-- ![Othello Gameplay Screenshot](assests\othello_game.jpg) -->

---

## Features

- Interactive **8x8 Othello board**
- Human vs. Human gameplay
- Human vs. AI gameplay
- AI opponent powered by **minimax**
- **Alpha-beta pruning** for faster AI decision-making
- Valid move highlighting
- Automatic disc flipping based on Othello rules
- Score tracking
- Win/loss display
- Undo functionality
- Turn-skipping when a player has no valid moves
- Simple graphical interface built with **Pygame**

---

## Technologies Used

- **Python 3.8+**
- **Pygame**
- Minimax Algorithm
- Alpha-Beta Pruning
- Object-Oriented Programming

---

## How the AI Works

The AI uses the **minimax algorithm** to look ahead at possible moves and choose the option that gives it the best advantage.

To improve performance, the AI also uses **alpha-beta pruning**, which reduces the number of unnecessary board states that need to be searched. This allows the AI to make stronger moves without checking every possible outcome.

---

## Installation

Make sure you have **Python 3.8 or newer** installed.

Clone the repository:

```bash
git clone https://github.com/your-username/your-repository-name.git