# Notes for Developers

## Setup

See the [recommended VS Code extensions](recommended_vscode_extensions.md) for a better dev experience.

### Via Local Environment

```bash
python -m venv venv
vim venv/bin/activate
# Then add line: export PYTHONPATH="$VIRTUAL_ENV/src"

source venv/bin/activate

pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
```

## 🤝 How to Contribute

We welcome contributions to the project!  
Here's how to get started — both through GitHub and your terminal.

### 📌 GitHub Setup

1. Fork the repository  
   Visit [the main repo](https://github.com/VladislavBalabaev/random_coffee_bot_telegram) and click **"Fork"** (top-right corner).

2. Clone your fork

   ```bash
   git clone https://github.com/<your-username>/random_coffee_bot_telegram.git
   cd random_coffee_bot_telegram
   ```

3. Add the original repo as `upstream`

   This keeps your fork in sync with the source:

   ```bash
   git remote add upstream https://github.com/VladislavBalabaev/random_coffee_bot_telegram.git
   ```

4. Check remotes

   ```bash
   git remote -v
   ```

### 💻 Workflow in Terminal

1. Create a new branch for your changes

   ```bash
   git checkout -b feature/your-change-name
   ```

2. Make edits, for example:

   ```bash
   nano docs/bot_logic/start_logic.md
   ```

3. Stage your changes

   ```bash
   git add docs/bot_logic/start_logic.md
   ```

4. Commit

   ```bash
   git commit -m "Improve start_logic.md docs"
   ```

5. Push to your fork

   ```bash
   git push origin feature/your-change-name
   ```

6. Open a Pull Request  
   Go to your fork on GitHub, and you’ll see a “Compare & pull request” button.

Happy contributing! 💙

### Via Docker Container

## Pre-Commit Actions

### Format & Lint

```bash
black src/ tests/

ruff check src/ tests/ --fix
```

### Type Check

```bash
mypy src/
```

### Run Tests

```bash
pytest
```

## Scripts

### To work with ChatGPT

Simple recursive script to walk through files and concatenate their contents with headers.

```bash
python scripts/combine_files.py
```

Additionally, you can use `tree` to show ChatGPT project's structure:

```bash
tree src/nespresso/
```
