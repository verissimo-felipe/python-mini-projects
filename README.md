# 🧠 Python Mini-Projects Collection

> A curated collection of small, focused Python projects designed for learning and skill development. Each project tackles a specific concept, library, or problem domain.

## 📝 Daily Log

See [`docs/`](docs/) for a day-by-day log of what was built and what each function does, one file per day (e.g. `docs/2026-07-20.md`).

## 📂 Project Directory

| Project | Description | Key Concepts | Done |
|---------|-------------|--------------|------|
| **ANSI Color Chart Generator** | Generates a chart of ANSI colors. | ANSI colors, print formatting, loops. | ✅ |
| **Tic-Tac-Toe (CLI)** | Classic Tic-Tac-Toe game played in the terminal. | Functions, lists, loops, conditional logic, basic game state management. | ✅ |
| **Hangman (CLI)** | Text-based Hangman game with random word selection. | Dictionaries, random module, string manipulation, input validation. | ✅ |
| **Password Generator** | Generates secure, random passwords with customizable length and complexity. | Random module, string constants, list comprehensions. | ✅ |
| **Dice Rolling Simulator** | Simulates rolling one or more dice with various face counts. | Random module, user input, statistical simulation. | ✅ |
| **Tip Calculator** | Calculates tips based on bill amount and service quality. | Floating-point arithmetic, user input, formatting. | ✅ |
| **Pomodoro Timer** | Time management tool using the Pomodoro Technique. | Time module, threading, loops, GUI with Tkinter. | ✅ |
| **BMI Calculator** | Calculates Body Mass Index and provides health insights. | Mathematical operations, conditional logic, health metrics. | ✅ |
| **Rock, Paper, Scissors** | Classic game against the computer. | Random module, conditional logic, user interaction. | ✅ |
| **Mad Libs Generator** | Fun word game creating silly stories. | String formatting (f-strings), user input. | ✅ |
| **Simple Calculator** | Basic four-function calculator with command-line interface. | Functions, user input, exception handling. | ✅ |
| **Unit Converter** | Converts between different units (e.g., Celsius/Fahrenheit, meters/feet). | Math operations, unit conversion formulas. | ✅ |
| **Markdown Previewer** | Preview Markdown files rendered as HTML. | Markdown library, file I/O, HTML generation. | ✅ |
| **Contact Book (CLI)** | Simple contact management system. | Dictionaries, lists, file I/O (JSON). | ✅ |
| **Number Guessing Game** | Guess a random number within a range. | Random module, loops, comparison operators. | ✅ |
| **Color Palette Generator** | Generates random color palettes with hex codes. | Random module, hex formatting, color theory basics. | ✅ |
| **To-Do List (CLI)** | Command-line task manager with due dates and completion status. | Lists, dictionaries, file I/O (JSON), datetime module. |
| **Expense Tracker** | Tracks expenses by category and summarizes monthly spending. | File I/O (CSV), dictionaries, basic statistics. |
| **Caesar Cipher Tool** | Encrypts and decrypts text using a classic Caesar cipher shift. | String manipulation, modular arithmetic. |
| **Weather CLI** | Fetches and displays the current weather for a city from a public API. | Requests library, JSON parsing, API consumption. |
| **Currency Converter** | Converts between currencies using live exchange rates from an API. | Requests library, JSON parsing, floating-point arithmetic. |
| **Typing Speed Test** | Measures typing speed (WPM) and accuracy against a sample text. | Time module, string comparison, user input. |
| **Quiz Game with Timer** | Multiple-choice quiz with a countdown timer per question. | Threading, dictionaries, scoring logic. |
| **Regex Validator** | Validates emails, phone numbers and other patterns using regular expressions. | Regex (re module), input validation. |
| **File Organizer** | Sorts files in a folder into subfolders by extension. | os/shutil modules, file system operations. |
| **Sorting Algorithm Visualizer** | Animates bubble sort, selection sort and quicksort step by step in the terminal. | Algorithms, recursion, ANSI colors. |

## 🚀 Getting Started

### Prerequisites
* **Python 3.6+**
* (Optional) `pip` for installing dependencies

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-mini-projects.git
   cd python-mini-projects
   ```

### Usage
Each project is self-contained. Navigate to the project directory and run the main script:

```bash
# Example: Run the Tic-Tac-Toe game
cd tic-tac-toe
python tic_tac_toe.py

# Example: Run the Password Generator
cd password-generator
python password_generator.py
```

A couple of projects (e.g. Markdown Previewer) need an extra third-party library. If a project folder has its own `requirements.txt`, install it first:
```bash
cd markdown-previewer
pip install -r requirements.txt
python markdown_previewer.py
```

## 🎓 How to Use This Repository for Learning

### For Beginners
1. **Pick a simple project**: Start with Tic-Tac-Toe or Dice Rolling Simulator
2. **Read the code**: Understand what each line does
3. **Run it**: See the program in action
4. **Modify it**: Change the code and observe the results
5. **Expand it**: Add new features (e.g., scorekeeping, difficulty levels)

### For Intermediate Developers
1. **Add OOP**: Convert procedural code to object-oriented
2. **Add GUI**: Replace CLI with a graphical interface (Tkinter, PyQt, or Kivy)
3. **Add Testing**: Write unit tests for each function
4. **Add Persistence**: Save data to files or databases
5. **Refactor**: Improve code structure and efficiency

## 📚 Key Concepts Covered

### Core Python
- Functions and modules
- Loops (for, while)
- Conditional statements (if/elif/else)
- Data structures (lists, dictionaries, sets)
- String manipulation
- File I/O (reading and writing files)
- Error handling (try/except)

### Libraries
- `random`: Random number generation, permutations, choices
- `time`: Time-related functions, delays
- `datetime`: Date and time operations
- `math`: Mathematical operations and constants
- `json`: JSON data serialization
- `os`: Operating system interactions

### Programming Paradigms
- Procedural programming
- Object-oriented programming (OOP) - can be added
- Event-driven programming (for GUI projects)

## 🤝 Contributing

Feel free to fork this repository, add your own mini-projects, or suggest improvements to existing ones. When adding a new project:

1. Create a new directory
2. Add a README explaining the project
3. Include comments in the code
4. Add docstrings to functions
5. Provide usage examples
6. Update this main README with project details

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Future Enhancements

- [ ] Add web-based versions using Flask or Django
- [ ] Integrate machine learning concepts
- [ ] Add database integration (SQLite, PostgreSQL)
- [ ] Include API integrations (weather, stocks, etc.)
- [ ] Add command-line argument parsing (argparse)

---

**Happy Coding!** 🐍✨
