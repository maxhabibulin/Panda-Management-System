# 🐼 Panda Spa Internal Management System (Demo)

This is an **educational Python project** created to practice backend design and object-oriented programming (OOP).
It simulates the **internal management system** of a fictional spa center - _Panda Spa_

---

## 💡 Features

- Manage and view internal spa services
- Handle customer appointments
- Display financial summaries
- Generate service recommendations
- Simple command-line interface (CLI)

---

## 🧱 Project Structure

```
panda_management_system/
│
├── data/                     # Demo data for services, appointments, and expenses
│   ├── services_data.py
│   ├── appointments_data.py
│   └── expenses_data.py
│
├── managers/                 # Core management modules
│   ├── services_manager.py
│   ├── appointments_manager.py
│   ├── finance_manager.py
│   └── recommendations_manager.py
│
├── utils/                    # Helper functions
│   ├── formatters.py
│   ├── validators.py
│
├── main.py                   # Main program entry point
├── LICENSE                   # MIT License
└── README.md

```

---

## 🚀 How to Run

1. Clone this repository:

```bash
git clone https://github.com/maxhabibulin/Panda-Management-System.git
cd panda_management_system
```

2. (Optional) Create a virtual environment:

```
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

3. Run the application:

```

python main.py

```

---

## 🗒️ Notes

- This is a **learning project** — not intended for production use.
- All data is stored in Python dictionaries for simplicity.
- Designed to demonstrate **modular architecture, separation of concerns, and clean OOP principles**.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Maksims Habibulins**

- 🐱 GitHub: [@maxhabibulin](https://github.com/maxhabibulin)
- 📧 Email: maxhabibulin@gmail.com

---

![Python](https://img.shields.io/badge/python-3.8+-blue.svg) ![Status](https://img.shields.io/badge/status-demo%20project-green.svg) ![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)
