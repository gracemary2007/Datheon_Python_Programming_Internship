# Datheon Python Programming Internship

Submission for the Datheon Python & AI Applications internship (4 weeks).
Author: Grace Mary Mannem

## Project Structure
```
Datheon_Python_Programming_Internship/
├── README.md
├── hangman.py          (Task 1)
├── portfolio.py        (Task 2)
├── prices.csv          (data for Task 2)
├── organizer.py        (Task 3)
├── chatbot.py          (Task 4)
└── faqs.json           (data for Task 4)
```

## Requirements
- Python 3.8 or newer
- Only the standard library is used. No installation needed.

## Task 1: Hangman Game
Console word-guessing game with ASCII gallows art. Pick random word, 6 allowed mistakes, repeated guesses are not penalised, play-again option.
```
python hangman.py
```
Concepts: `random`, sets, loops, string handling.

## Task 2: Stock Portfolio Tracker
Enter tickers, buy price and quantity. Current prices come from `prices.csv` (or manual entry). Shows value and % gain/loss per holding and totals, then writes `portfolio_summary.csv`.
```
python portfolio.py
```
Concepts: dictionaries, `csv` module, file I/O, input validation.

## Task 3: File Organizer
Sorts files in a folder into Documents, Images, Videos, Audio, Archives, Code and Others. Renames duplicates as `name (1).ext`, handles permission errors, prints a summary.
```
python organizer.py "path/to/folder" --dry-run   # preview
python organizer.py "path/to/folder"             # organize
```
Concepts: `pathlib`, `shutil`, `argparse`, `logging`, exception handling.

## Task 4: Rule-Based Chatbot
Terminal assistant that matches regex patterns from `faqs.json` (hours, shipping, returns, prices, payment, contact). Handles several questions in one message, has a fallback reply, and exits on `bye`, `exit` or `quit`.
```
python chatbot.py
```
Concepts: `re`, `json`, functions, input normalization.

## Demo
LinkedIn walkthrough: _add link here_
