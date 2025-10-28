# 🐼 Panda Spa Internal Management System (Demo)

This is an **educational Python project** created to practice backend design and object-oriented programming (OOP).
It simulates the internal management system of a fictional spa center - _Panda Spa_

---

## 💡 Features

- Manage and view internal spa services
- Handle customer appointments
- Display financial summaries
- Generate service recommendations
- Simple command-line interface (CLI)

---

## 🧱 Project Structure

- **panda_management_system/**

  - main.py # Main program entry

  - **data/** # Demo data for services, appointments, and expenses

    - services_data.py
    - appointments_data.py
    - expenses_data.py

  - **managers/** # Core management modules
    - services_manager.py
    - appointments_manager.py
    - finance_manager.py
    - recommendations_manager.py

---

## 🚀 How to Run

1. Clone this repository:

```
bash
git clone https://github.com/maxhabibulin/Panda-Management-System
cd panda_management_system
```

2. (Optional) Create a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

3. Run the application:

```
python main.py
```

---

## 🗒️ Notes

- This is _learning project_ - not intended for production use.
- All data is stored in Python dictionaries for simplicity.

* Designed for educational purposes to demonstrate modular structure and clean design.

---

## Author

Developed by Max Habibulin
GitHub: maxhabibulin
