# 💰 Expense Tracker (Django)

A simple and secure **Expense Tracking Web Application** built with the **Django Framework**, designed to help users **record, manage, and visualize** their daily expenses through an elegant dashboard and interactive charts powered by **Plotly**.

---

## ⚙️ Features Overview

| Feature | Description |
|----------|-------------|
| 🔐 Authentication | User signup, login, and logout with Django Auth |
| 💸 Expense Management | Add, edit, and delete expenses per user |
| 🗓️ Filtering | Filter by category and date range |
| 📅 Monthly Summary | Shows total spending for the current month |
| 📊 Analytics | Pie and Line charts using Plotly |
| 🧭 Access Control | Only authenticated users can access their own data |
| 💻 Admin Panel | Full control via Django Admin interface |

---

## 🧩 Project Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/pankajrajparajuli/expense_tracker_django-internship-.git
cd expense_tracker
```

### 2️⃣ Create Virtual Environment & Activate
```bash
python -m venv venv
```

Activate it:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6️⃣ Start the Server
```bash
python manage.py runserver
```

> Visit **http://127.0.0.1:8000** to use the app.

---

## 🧪 Testing the Application

| Step | Action | Description |
|------|---------|-------------|
| 🧍‍♂️ 1 | `/signup/` | Register a new user |
| 🔑 2 | `/login/` | Log in to access your dashboard |
| ➕ 3 | `/expenses/create/` | Add a new expense |
| 📋 4 | `/expenses/` | View and filter expenses by date/category |
| ✏️ 5 | `/expenses/edit/<id>/` | Edit existing expense |
| ❌ 6 | `/expenses/delete/<id>/` | Delete expense entry |
| 📊 7 | `/expenses/dashboard/` | View analytics with daily/weekly charts |

---

## 🧑‍💼 Admin APIs (Django Admin Panel)

| Access | URL | Description |
|--------|-----|-------------|
| GET | `/admin/` | Admin login dashboard |
| GET | `/admin/auth/user/` | Manage all registered users |
| GET | `/admin/expenses/expense/` | View or delete any expense record |

> ℹ️ All admin endpoints are accessible via the Django admin panel.  
> Requires login with **superuser credentials**.

---

## 🧪 Other Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | `/` | Homepage redirect (login/signup) |
| GET | `/expenses/dashboard/` | Main analytics dashboard |
| GET | `/expenses/` | Expense list (paginated) |

---

## 📦 Tech Stack

| Component | Technology |
|------------|-------------|
| **Language** | Python 3.10+ |
| **Framework** | Django 5.x |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3, Plotly.js |
| **Authentication** | Django’s built-in Auth |
| **Testing** | Django TestCase, pytest |
| **Version Control** | Git & GitHub |

---

## 🚀 How to Use

1. **Create your account**
   ```bash
   Go to http://127.0.0.1:8000/signup/
   ```

2. **Log in**
   ```bash
   Go to http://127.0.0.1:8000/login/
   ```

3. **Add an expense**
   - Choose category, amount, and title.
   - Save to view it in the list and dashboard.

4. **View the Dashboard**
   - Access **http://127.0.0.1:8000/expenses/dashboard/**
   - View pie charts (category breakdown) and line charts (daily/weekly).

5. **Access Admin Panel**
   ```bash
   Go to http://127.0.0.1:8000/admin/
   ```
   Log in with superuser credentials to manage users and expenses.

---

## 🧪 Run Tests

Run unit tests for all expense-related views and authentication:
```bash
python manage.py test expenses
```

---

## 🧾 Example Commands

| Task | Command |
|------|----------|
| Run the application | `python manage.py runserver` |
| Run migrations | `python manage.py migrate` |
| Create superuser | `python manage.py createsuperuser` |
| Generate requirements.txt | `pip freeze > requirements.txt` |

---

## 📁 Project Structure

```
expense-tracker/
│
├── expenses/
│   ├── migrations/
│   ├── templates/
│   │   └── expenses/
│   │       ├── dashboard.html
│   │       ├── expense_list.html
│   │       ├── expense_form.html
│   │       ├── expense_confirm_delete.html
│   │       └── signup.html
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── admin.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧠 Design Approach

- Based on Django’s **Model–View–Template (MVT)** pattern  
- Uses `LoginRequiredMixin` and `UserPassesTestMixin` for authentication control  
- Data visualized with **Plotly** charts for interactivity  
- All expense operations scoped to each authenticated user  
- Clean UI with unified color scheme and consistent typography  

---
## 🧪 Steps to Test the Application (Login, Add, Edit, Delete Expense)

Follow these steps to verify the main features of the Expense Tracker:

### 1. Sign Up or Log In
- Visit: [http://127.0.0.1:8000/signup/](http://127.0.0.1:8000/signup/)
- Create a new account.
- After registration, you’ll be redirected to the **Dashboard**.
- If you already have an account, go to `/login/` and sign in.

### 2. Add an Expense
- Navigate to **“Add Expense”** from the top navigation bar.
- Enter the following details:
  - **Title:** Short name of the expense (e.g., “Lunch”)
  - **Amount:** Any positive value (e.g., `25`)
  - **Category:** Choose from available categories (e.g., “Food”)
- Click **Save** — you’ll see a success message confirming it’s added.

### 3. View All Expenses
- Go to the **Expense List** page (`/expenses/`).
- Check that your new expense appears in the list.
- Use **filters** (date or category) to narrow down the results.
- At the top, the total monthly spending is displayed.

### 4. Edit an Expense
- In the expense list, click **Edit** next to an entry.
- Update any field (e.g., change the amount from `25` to `30`).
- Click **Save** — verify that the change reflects in the table and dashboard.

### 5. Delete an Expense
- From the list, click **Delete** next to an expense.
- Confirm deletion on the confirmation page.
- Verify that it disappears from the list and total updates accordingly.

### 6. Dashboard Verification
- Visit `/expenses/dashboard/`
- Check:
  - Total monthly spending
  - Top spending category
  - Interactive Pie and Line Charts (daily/weekly toggle)

✅ **Expected Result:**  
All CRUD operations (Create, Read, Update, Delete) should work smoothly, and the dashboard should update automatically after each change.


## 🧑‍💻 Author

**Pankaj Raj Parajuli**  
💼 Django Developer & Software Engineer  
📧 Email: pankajrajparajuli@gmail.com 
🌐 GitHub: [github.com/pankajrajparajuli](https://github.com/pankajrajparajuli)

---


## 🏁 Quick Recap

✅ **Login Required:** All expense pages restricted to authenticated users  
✅ **User Ownership:** Users only manage their own expenses  
✅ **Charts:** Dynamic daily/weekly visualization with Plotly  
✅ **UI:** Clean and responsive  
✅ **Tests:** Full CRUD and authentication coverage  

---

> _“Track wisely. Spend smartly.”_ 💸
