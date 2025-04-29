💰 Budget Tracker (Django Project)
This is a personal finance tracker built with Django.
You can add income and expenses, visualize summaries with pie and bar charts, and filter entries by month!

🚀 Getting Started
Clone the repository

git clone https://github.com/yourusername/your-repo-name.git

cd your-repo-name

Set up a virtual environment

python -m venv venv

Activate it:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Apply migrations

python manage.py migrate

(Optional) Create a superuser

python manage.py createsuperuser

(Needed if you want to access Django admin.)


Run the server

python manage.py runserver

Visit: http://127.0.0.1:8000/


📊 Features

Add/Edit/Delete income and expenses

View total income, expenses, and remaining balance

Pie chart for expense breakdown by category

Bar chart for monthly income vs expenses

Filter entries by month

User authentication (login/logout/register)


🛠 Built With

Django 5.2

Python 3.13

SQLite (default database)

Bootstrap 5 (for styling)

Chart.js (for graphs)


📂 Project Structure
budget_tracker/
├── config/ 
├── tracker/ 
├── templates/ 
├── venv/ 
├── db.sqlite3 # Local database
├── manage.py
└── requirements.txt

🙋‍♂️ Notes
Make sure you are using Python 3.11+ or 3.13
Virtual environment is recommended
Do not push venv/ or db.sqlite3 into GitHub (use .gitignore)


📜 License
This project is for educational purposes only.


⚡ Quick Start Commands

git clone https://github.com/yourusername/your-repo-name.git

cd your-repo-name

python -m venv venv

venv\Scripts\activate (or source venv/bin/activate)

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

