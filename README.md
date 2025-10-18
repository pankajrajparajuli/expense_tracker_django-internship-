echo "# 💰 Expense Tracker (Django)

A simple and elegant web application built with **Django** that allows users to track their daily expenses — add, edit, delete, and visualize spending through interactive charts.

## 🚀 Features
- User authentication (signup, login, logout)
- Add, edit, and delete expenses
- Filter expenses by category and date
- Monthly total and category-wise summaries
- Interactive charts using **Plotly**
- Secure per-user data access

## ⚙️ Setup Instructions
### 1️⃣ Create a Virtual Environment
\`\`\`bash
python -m venv venv
venv\\Scripts\\activate  # on Windows
source venv/bin/activate # on macOS/Linux
\`\`\`

### 2️⃣ Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3️⃣ Apply Migrations & Run Server
\`\`\`bash
python manage.py migrate
python manage.py runserver
\`\`\`

### 4️⃣ Create Superuser
\`\`\`bash
python manage.py createsuperuser
\`\`\`

Visit http://127.0.0.1:8000 to start using the app!

## 🧪 Testing
\`\`\`bash
python manage.py test expenses
\`\`\`

## 🧠 Approach
Built using Django’s MVT architecture, leveraging:
- Django auth system for secure user access
- Plotly for visual analytics
- LoginRequiredMixin & UserPassesTestMixin for data protection
- SQLite as lightweight DB backend

## 👨‍💻 Author
**Pankaj Raj Parajuli**

