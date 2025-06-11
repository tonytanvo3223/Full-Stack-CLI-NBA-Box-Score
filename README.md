# Full-Stack CLI NBA Box Score

This project is a custom-built basketball data management application that allows users to insert, manage, and query detailed NBA game statistics. It was designed as a learning and portfolio-building project that combines backend database design with frontend logic powered by AI-generated code.

---

## 💡 Project Overview

This system enables users to:

1. **Search for NBA games** by date or team
2. **Insert new games and player stats**
3. **View team and individual statistics** in a clean tabular format
4. **Manage player rosters** including adding, updating, or removing players

The system also automatically calculates team stats (e.g., shooting percentages, fouls, rebounds) based on individual player data and reflects game states (Final or Not Started).

---
## 📁 Repository Structure
├── Code/
│   ├── base_code_nba.py             # SQLAlchemy schema and base setup
│   ├── insert_nba_data.py           # CLI tool for inserting games and stats
│   └── nba_box_score.py             # Logic for querying and displaying stats
│
├── Database/
│   ├── NBA.db                       # Main database: teams, games, players
│   └── NBA_BoxScore.db              # Box score tracking for each game
│
├── Document/
│   ├── AIprompts.pdf                # Prompt logs for Claude and ChatGPT
│   ├── NBA Box Score.pdf            # User-facing box score reference
│   ├── annotatedRequirements.pdf    # Schema constraints and business rules
│   └── reflection.pdf               # Project development reflection
│
├── .gitignore                       # Files to ignore in Git tracking
├── LICENSE                          # MIT License
└── README.md                        # Project overview (this file)

---

## 🧠 AI Collaboration

We leveraged state-of-the-art large language models to assist in code generation and system design:
- **Anthropic Claude 3.5 Sonnet**: Used for generating clean, modular Python logic.
- **OpenAI ChatGPT-4o**: Used for building and refactoring SQLAlchemy-based backend and table display logic.

Prompts and iterations used in development are documented in `AIprompts.pdf`.

---

## 🧪 Features & Logic

- ✅ Auto-incrementing game and player IDs
- ✅ Computed team stats from player stats (e.g., FG%, FT%, rebounds, turnovers)
- ✅ Contextual game info: show schedule, results, and stats only for completed games
- ✅ Conditional UI: "Final" games allow stat views, "Not Started" do not
- ✅ Smart search by team/date with formatted game summaries

---

## 📌 Requirements Summary

Outlined in `annotatedRequirements.pdf`, the schema enforces:
- One-to-many player-team relationships
- Unique player-game stat entries
- Boolean flags for starters and on-court presence
- Accurate win tracking and team/game associations

---

## 👥 Authors

- **Tan Vo**  
- **Jonathan Roux**
