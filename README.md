# 💰 Budget Tracker (Django Project)

A simple yet powerful personal finance tracker built with Django.  
Track your income and expenses, visualize spending patterns, and stay on top of your budget goals with ease.

---

## 🚀 Getting Started

Follow these steps to get the project up and running locally:

### 1. Clone the Repository
```bash
git clone https://github.com/sipatrickito/CMSC126_LE2_Budget_Tracker.git
cd CMSC126_LE2_Budget_Tracker
```

### 2. Set Up a Virtual Environment

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. (Optional) Create a Superuser
```bash
python manage.py createsuperuser
```
> Needed if you want to access the Django admin panel at `/admin`.

### 6. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and visit:  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📊 Features

- ➕ Add, ✏️ Edit, and ❌ Delete income or expense entries
- 📅 Filter entries by month
- 📈 Bar chart for **monthly income vs expenses**
- 🥧 Pie chart for **expense breakdown by category**
- 💼 Set budgets per category and track overspending
- 🧾 Export entries to CSV (with filters)
- 🔐 User authentication (login/register/logout)
- 📂 Category-based organization of entries

---

## 🛠 Built With

- **Django 5.2**
- **Python 3.13**
- **SQLite** – default database (easy setup)
- **Bootstrap 5** – for responsive UI
- **Chart.js** – for data visualization

---

## 📂 Project Structure

```
budget_tracker/
├── config/                 # Project settings
├── tracker/                # Core app (models, views, urls)
├── templates/              # HTML templates
├── venv/                   # Virtual environment (excluded from Git)
├── db.sqlite3              # Local database
├── manage.py               # Django CLI
└── requirements.txt        # Python dependencies
```

---

## 🙋‍♂️ Notes

- ✅ Use **Python 3.11+** (Tested on Python 3.13)
- ✅ Always activate your virtual environment
- 🛑 Don’t commit `venv/` or `db.sqlite3` to GitHub (use `.gitignore`)
- ⚙️ You can access Django admin at `/admin` after creating a superuser

---

## 📤 Export to CSV

From the homepage, click **"Export to CSV"** to download your filtered income and expense data.

You can filter by:
- 📆 Month
- 📂 Category

---

## 📜 License

This project is for **educational purposes only** and not intended for production use.

---

## ⚡ Quick Start Commands (Recap)
```bash
git clone https://github.com/sipatrickito/CMSC126_LE2_Budget_Tracker.git
cd CMSC126_LE2_Budget_Tracker
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Happy budgeting! 💸
