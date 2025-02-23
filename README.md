# Flappy Koala 🐨

A simple Flappy Bird-style game implemented in Python using Pygame.

## Description

Flappy Koala is a game where you control a flying koala, helping it navigate through the trees by flapping. The goal is to survive as long as possible and achieve the highest score.

## Prerequisites

- Python 3.8 or higher
- Pygame
- PyInstaller (for building executable)

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/flappy-koala.git
   cd flappy-koala
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv

   # On Windows:
   .\venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

## Building Executable

### For Windows

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Build executable
pyinstaller flappy.spec --clean --noconfirm

# Executable will be in dist/FlappyGame.exe
```

### For macOS

```bash
# Activate virtual environment
source venv/bin/activate

# Build executable
pyinstaller flappy.spec --clean --noconfirm

# App will be in dist/FlappyGame.app
```

## Distribution

### Windows

1. Navigate to `dist` folder
2. Zip the `FlappyGame.exe` and its supporting files
3. Share the zip file

### macOS

1. Navigate to `dist` folder
2. Right-click on `FlappyGame.app` and select "Compress"
3. Share the resulting zip file

## How to Play

1. Run the game:

   Development:

   ```bash
   python app.py
   ```

   Or run the executable:

   - Windows: Double-click `FlappyGame.exe`
   - macOS: Double-click `FlappyGame.app`

2. Press SPACE to make the koala flap
3. Avoid hitting the pipes and the screen boundaries
4. Try to get the highest score possible!

## Controls

- SPACE: Flap
- Close window to quit

## Troubleshooting

### macOS distribution

If you get a security warning:

1. Go to System Preferences > Security & Privacy
2. Click "Open Anyway" for FlappyGame.app

### Windows distribution

If you get a SmartScreen warning:

1. Click "More info"
2. Click "Run anyway"

## License

This project is licensed under the MIT License - see the LICENSE file for details.
