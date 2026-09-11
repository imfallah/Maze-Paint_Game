<p align="center">
  <img src="https://raw.githubusercontent.com/imfallah/Maze-Paint_Game/main/public/banner.png" width="900" alt="MazePaint Banner">
</p>

# 🎨 MazePaint

<p align="center">

### **Explore. Solve. Paint. Compete.**

A modern 2D maze adventure game built with **Python, PyQt5 and Pygame**.

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/PyQt5-Desktop_UI-41CD52?style=for-the-badge&logo=qt&logoColor=white">
  <img src="https://img.shields.io/badge/Pygame-Game_Engine-1B1B1B?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Supabase-Online-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white">
</p>

<p>
  <img src="https://img.shields.io/github/stars/imfallah/Maze-Paint_Game?style=flat-square">
  <img src="https://img.shields.io/github/forks/imfallah/Maze-Paint_Game?style=flat-square">
  <img src="https://img.shields.io/github/issues/imfallah/Maze-Paint_Game?style=flat-square">
  <img src="https://img.shields.io/github/license/imfallah/Maze-Paint_Game?style=flat-square">
</p>

</p>

---

## 📸 Game Preview

<p align="center">
  <img src="./public/main.png" alt="MazePaint Main Menu" width="30%">
  <img src="./public/game.png" alt="MazePaint Gameplay" width="30%">
  <img src="./public/level-s2.png" alt="MazePaint Level Selection" width="30%">
</p>

<p align="center">
  <img src="./public/Profile.png" alt="MazePaint Profile" width="30%">
  <img src="./public/leaderboard.png" alt="MazePaint Leaderboard" width="30%">
  <img src="./public/chat_box.png" alt="MazePaint Chat" width="30%">
</p>

<p align="center">
  <img src="./public/maingif.gif" alt="MazePaint Gameplay Preview" width="650">
</p>

<p align="center">
  <i>MazePaint gameplay and interface preview.</i>
</p>

---

<a id="contents"></a>

# 📚 Contents

* [📥 Downloads](#downloads)
* [✨ Features](#features)
* [🛠️ Built With](#built-with)
* [🏗️ Architecture](#architecture)
* [📁 Project Structure](#project-structure)
* [🗺️ Level System](#level-system)
* [⭐ Star System](#star-system)
* [💾 Save System](#save-system)
* [🌐 Online Features](#online-features)
* [🎮 Controls](#controls)
* [🚀 Run From Source](#run-from-source)
* [🪟 Windows Build](#windows-build)
* [🐧 Linux](#linux)
* [📦 Releases](#releases)
* [⚙️ Configuration](#configuration)
* [🔧 Development](#development)
* [🗺️ Roadmap](#roadmap)
* [🐛 Known Issues](#known-issues)
* [🤝 Contributing](#contributing)
* [📄 License](#license)
* [👨‍💻 Creator](#creator)

---

<a id="downloads"></a>

## 📥 Downloads

Pre-built versions are available through **GitHub Releases**.

| Platform        | Package                | Status               |
| --------------- | ---------------------- | -------------------- |
| 🪟 Windows      | Standalone application | ✅ Available          |
| 🐧 Linux        | Standalone application | ✅ Available          |
| 📦 Linux `.deb` | [Debian package](https://github.com/imfallah/Maze-Paint_Game-PYQT5/releases/download/v1.0.0/MazePaint_1.0.0_amd64.deb)     | ✅ Available   |
| 📦 AppImage     | [AppImage package](https://github.com/imfallah/Maze-Paint_Game-PYQT5/releases/download/v1.0.0/MazePaint-x86_64.AppImage) | ✅Available           |

### ⬇️ Download

**[🚀 View All Releases](https://github.com/imfallah/Maze-Paint_Game/releases)**

> For Windows and Linux, download the latest release package and follow the included instructions.

---

<a id="features"></a>

## ✨ Features

### 🧩 Gameplay

* 🎮 Interactive 2D maze gameplay
* 🗺️ Multiple handcrafted levels
* 🔓 Progressive level unlocking
* ⭐ Star-based performance system
* 🏆 Level completion tracking
* 👑 Special Boss level
* 🌦️ Environmental effects
* 🌀 Special movement and visual effects
* 📈 Increasing difficulty

### 👤 Player System

* 👤 Player profiles
* ✏️ Custom player names
* 💾 Local progress saving
* 🔓 Level unlock tracking
* 🏆 Completed-level tracking
* ⭐ Star records
* 👥 Separate player data for multiple local instances

### 🌐 Online Features

* 🏆 Online leaderboard
* 🟢 Player presence
* 💬 Player-to-player messaging
* ☁️ Supabase-powered services
* 🔄 Online player information

### 🎨 User Interface

* 🌙 Modern dark-themed UI
* 🪟 Custom title bar
* 🎛️ Rounded animated buttons
* ✨ Hover animations
* 👤 Profile interface
* ⚙️ Settings interface
* 🏆 Leaderboard interface
* 💬 Chat interface
* 🎮 Integrated Pygame game window
* 🚀 Dedicated splash screen

---

<a id="built-with"></a>

## 🛠️ Built With

| Technology         | Purpose                          |
| ------------------ | -------------------------------- |
| 🐍 **Python**      | Core programming language        |
| 🎨 **PyQt5**       | Desktop user interface           |
| 🎮 **Pygame**      | Game engine and rendering        |
| 📄 **JSON**        | Level definitions and local data |
| ☁️ **Supabase**    | Online services                  |
| 📦 **PyInstaller** | Application packaging            |
| 🔧 **Git**         | Version control                  |
| 🐙 **GitHub**      | Source code and releases         |

---

<a id="architecture"></a>

## 🏗️ Architecture

MazePaint combines a **PyQt5 desktop interface** with a **Pygame gameplay engine**.

```text
                         ┌──────────────────────┐
                         │       MazePaint      │
                         │       main.py        │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  │                                   │
          ┌───────▼────────┐                 ┌────────▼────────┐
          │    PyQt5 UI    │                 │  Pygame Engine  │
          │                 │                 │                 │
          │ Main Menu       │                 │ Maze            │
          │ Profile         │                 │ Player          │
          │ Settings        │                 │ Gameplay        │
          │ Leaderboard     │                 │ Rendering       │
          │ Chat            │                 │ Effects         │
          └───────┬─────────┘                 └────────┬────────┘
                  │                                    │
                  └────────────────┬───────────────────┘
                                   │
                         ┌─────────▼─────────┐
                         │  Data & Services  │
                         │                   │
                         │ Level Manager     │
                         │ Save Manager      │
                         │ JSON Data         │
                         │ Supabase API      │
                         └───────────────────┘
```

### Core Components

| Component                 | Responsibility                  |
| ------------------------- | ------------------------------- |
| `main.py`                 | Application entry point         |
| `splash_screen.py`        | Startup splash screen           |
| `game/game.py`            | Main gameplay logic             |
| `game/maze.py`            | Maze generation and handling    |
| `game/player.py`          | Player state and movement       |
| `game/level_manager.py`   | Level loading and progression   |
| `game/save_manager.py`    | Local progress persistence      |
| `game/leaderboard_api.py` | Online leaderboard and services |
| `game/pygame_widget.py`   | Pygame integration with PyQt5   |
| `levels/*.json`           | Level definitions               |

---

<a id="project-structure"></a>

## 📁 Project Structure

```text
MazePaint/
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── ...
│
├── game/
│   ├── game.py
│   ├── maze.py
│   ├── player.py
│   ├── level_manager.py
│   ├── leaderboard_api.py
│   ├── pygame_widget.py
│   ├── save_manager.py
│   └── ...
│
├── levels/
│   ├── level_01.json
│   ├── level_02.json
│   ├── level_03.json
│   └── ...
│
├── public/
│   ├── main.png
│   ├── game.png
│   ├── level-s2.png
│   ├── Profile.png
│   ├── leaderboard.png
│   ├── chat_box.png
│   └── maingif.gif
│
├── main.py
├── splash_screen.py
├── MazePaint.spec
├── requirements.txt
└── README.md
```

---

<a id="level-system"></a>

## 🗺️ Level System

MazePaint uses **JSON-based level definitions**, allowing levels to be created and modified without changing the core gameplay code.

### Difficulty Progression

```text
┌───────────────────────────────────────┐
│  LEVEL 01 - 05     🟢 EASY           │
├───────────────────────────────────────┤
│  LEVEL 06 - 10     🟡 MEDIUM         │
├───────────────────────────────────────┤
│  LEVEL 11 - 15     🟠 HARD           │
├───────────────────────────────────────┤
│  LEVEL 16 - 19     🔴 VERY HARD      │
├───────────────────────────────────────┤
│  LEVEL 20          👑 BOSS           │
└───────────────────────────────────────┘
```

Each level can contain its own:

* Maze layout
* Gameplay configuration
* Difficulty
* Completion requirements
* Visual/environmental settings

This structure makes the game easier to expand with new levels.

---

<a id="star-system"></a>

## ⭐ Star System

Players can earn up to **three stars** based on their performance.

```text
⭐        Completed
⭐⭐      Good Performance
⭐⭐⭐    Excellent Performance
```

Stars are stored locally and associated with the player's progress.

---

<a id="save-system"></a>

## 💾 Save System

MazePaint stores player progress locally.

A typical save structure looks like:

```json
{
    "unlocked": 1,
    "completed": [],
    "stars": {}
}
```

The save system tracks:

* 🔓 Unlocked levels
* 🏆 Completed levels
* ⭐ Earned stars

### Multiple Game Instances

MazePaint can separate player-specific data using an instance identifier.

Example:

```bash
MAZEPAINT_INSTANCE=player1
```

This allows multiple local game instances to maintain independent player information.

---

<a id="online-features"></a>

## 🌐 Online Features

MazePaint communicates with online services through **Supabase**.

```text
                       MazePaint
                           │
                           ▼
                    Leaderboard API
                           │
                           ▼
                       Supabase
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
       Leaderboard       Chat         Presence
```

### Online Services

* 🏆 Leaderboard
* 🟢 Player presence
* 💬 Player messaging
* 👥 Online player information

> Online features require the appropriate Supabase configuration.

---

<a id="controls"></a>

## 🎮 Controls

| Key       | Action         |
| --------- | -------------- |
| `W` / `↑` | Move Up        |
| `S` / `↓` | Move Down      |
| `A` / `←` | Move Left      |
| `D` / `→` | Move Right     |
| `ESC`     | Pause / Return |

> Additional controls may be introduced as new gameplay mechanics are added.

---

<a id="run-from-source"></a>

## 🚀 Run From Source

### 1. Clone the Repository

```bash
git clone https://github.com/imfallah/Maze-Paint_Game.git
cd Maze-Paint_Game
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start MazePaint

```bash
python main.py
```

---

<a id="windows-build"></a>

## 🪟 Windows Build

MazePaint can be packaged into a standalone Windows application using **PyInstaller**.

```bash
pyinstaller MazePaint.spec
```

The generated application will be located inside:

```text
dist/
```

For the onedir build, distribute the **entire generated MazePaint directory**, not only the `.exe` file.

Example:

```text
dist/
└── MazePaint/
    ├── MazePaint.exe
    └── _internal/
        ├── ...
        └── levels/
```

> ⚠️ Do not copy only `MazePaint.exe`. The `_internal` directory contains required runtime files and dependencies.

---

<a id="linux"></a>

## 🐧 Linux

MazePaint can be run directly from source:

```bash
python3 main.py
```

Or packaged using PyInstaller:

```bash
pyinstaller MazePaint.spec
```

The generated application will be available inside:

```text
dist/
```

Linux packages such as `.deb` or AppImage can be distributed through GitHub Releases.

---

<a id="releases"></a>

## 📦 Releases

Official builds are published through:

**[🚀 MazePaint Releases](https://github.com/imfallah/Maze-Paint_Game/releases)**

Possible release formats include:

```text
Windows
└── MazePaint.zip

Linux
├── MazePaint.tar.gz
├── mazepaint.deb
└── MazePaint.AppImage
```

Release availability may vary between versions.

---

<a id="configuration"></a>

## ⚙️ Configuration

Online services can be configured using environment variables.

Example:

```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 🔐 Security

Never commit private credentials or secrets to GitHub.

Use environment variables or another secure configuration method for sensitive information.

---

<a id="development"></a>

## 🔧 Development

Clone the project:

```bash
git clone https://github.com/imfallah/Maze-Paint_Game.git
cd Maze-Paint_Game
```

Create a development environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the game:

```bash
python main.py
```

### Development Workflow

```text
Create Feature
     │
     ▼
Create Branch
     │
     ▼
Implement Changes
     │
     ▼
Test Locally
     │
     ▼
Commit Changes
     │
     ▼
Push Branch
     │
     ▼
Open Pull Request
```

---

<a id="roadmap"></a>

## 🗺️ Roadmap

### ✅ Completed

* [x] Core maze gameplay
* [x] PyQt5 interface
* [x] Pygame integration
* [x] Level management
* [x] Local save system
* [x] Player profiles
* [x] Star system
* [x] Leaderboard system
* [x] Online presence
* [x] Chat architecture
* [x] Windows packaging
* [x] Linux build support

### 🚧 Planned

* [ ] More maze levels
* [ ] Achievements system
* [ ] Sound effects
* [ ] Background music
* [ ] More environmental effects
* [ ] Advanced player statistics
* [ ] Improved online synchronization
* [ ] More gameplay animations
* [ ] Expanded multiplayer features
* [ ] Steam / game-store distribution

---

<a id="known-issues"></a>

## 🐛 Known Issues

MazePaint is an actively developed project.

Some online functionality and environmental effects may still be under development and can change between releases.

If you encounter a problem, please open an issue:

**[🐛 Report a Bug](https://github.com/imfallah/Maze-Paint_Game/issues)**

When reporting an issue, include:

* Operating system
* Python version
* MazePaint version
* Steps to reproduce the problem
* Error message or screenshot, if available

---

<a id="contributing"></a>

## 🤝 Contributing

Contributions are welcome!

### Contribution Steps

**1. Fork the repository**

**2. Create a feature branch**

```bash
git checkout -b feature/my-feature
```

**3. Make your changes**

**4. Test your changes**

**5. Commit**

```bash
git commit -m "Add new feature"
```

**6. Push your branch**

```bash
git push origin feature/my-feature
```

**7. Open a Pull Request**

Please keep pull requests focused and include a clear description of the changes.

---

<a id="license"></a>

## 📄 License

MazePaint is currently an actively developed project.

A formal open-source license will be added before the first stable public release.

Until then, please refer to the repository for the current project status and usage terms.

---

<a id="creator"></a>

## 👨‍💻 Creator

### Mohammad Fallahnejad

**Python Developer • Game Developer • Linux Enthusiast**

<p>
  <a href="https://github.com/imfallah">
    <img src="https://img.shields.io/badge/GitHub-imfallah-181717?style=for-the-badge&logo=github">
  </a>
</p>

---

## ⭐ Support the Project

If you like MazePaint, consider giving the repository a ⭐ on GitHub.

Every star helps the project gain visibility and motivates further development.

<p align="center">

### 🎨 MazePaint

**Explore. Solve. Paint. Compete.**

Made with ❤️ using **Python, PyQt5 and Pygame**.

</p>

---

<p align="center">
  <sub>© MazePaint • Built with Python</sub>
</p>
