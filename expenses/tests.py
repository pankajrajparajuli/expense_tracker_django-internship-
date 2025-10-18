from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Expense


class ExpenseViewsTest(TestCase):
    """Test suite for Expense Tracker views."""

    def setUp(self):
        """Set up test user and sample data."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

        # Sample expenses
        Expense.objects.create(user=self.user, title='Lunch', amount=100, category='Food')
        Expense.objects.create(user=self.user, title='Bus', amount=20, category='Transport')

    # =============================
    # 🧍‍♂️ Signup / Login / Logout
    # =============================

    def test_signup_view(self):
        """User can sign up successfully."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpass123!',
            'password2': 'newpass123!',
        })
        self.assertEqual(response.status_code, 302)  # redirect to login
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_redirects_to_dashboard(self):
        """Successful login redirects to dashboard."""
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_logout(self):
        """Logout should redirect to login with message."""
        response = self.client.get(reverse('custom_logout'))
        self.assertRedirects(response, reverse('login'))

    # =============================
    # 📊 Dashboard
    # =============================

    def test_dashboard_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_renders_for_logged_user(self):
        """Authenticated users can view their dashboard."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/dashboard.html')
        self.assertContains(response, 'Expense Dashboard')
        self.assertContains(response, 'Hi, Testuser')

    # =============================
    # 📋 Expense List View
    # =============================

    def test_expense_list_view_loads(self):
        """Expense list view should render correctly."""
        response = self.client.get(reverse('expense-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/expense_list.html')
        self.assertContains(response, 'Lunch')
        self.assertContains(response, 'Bus')

    def test_expense_list_filter_by_category(self):
        """Filtering by category should limit results."""
        response = self.client.get(reverse('expense-list'), {'category': 'Food'})
        self.assertContains(response, 'Lunch')
        self.assertNotContains(response, 'Bus')

    # =============================
    # ➕ Expense Create View
    # =============================

    def test_create_expense(self):
        """User can create a new expense."""
        response = self.client.post(reverse('expense-create'), {
            'title': 'Groceries',
            'amount': 200,
            'category': 'Food',
        })
        self.assertRedirects(response, reverse('expense-list'))
        self.assertTrue(Expense.objects.filter(title='Groceries').exists())

    def test_create_invalid_amount(self):
        """Invalid amount (<=0) should show error."""
        response = self.client.post(reverse('expense-create'), {
            'title': 'Invalid',
            'amount': -10,
            'category': 'Food',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amount must be greater than 0.")

    # =============================
    # ✏️ Expense Update View
    # =============================

    def test_update_expense(self):
        """User can update an expense."""
        expense = Expense.objects.first()
        response = self.client.post(reverse('expense-edit', args=[expense.id]), {
            'title': 'Updated Lunch',
            'amount': 150,
            'category': 'Food',
        })
        self.assertRedirects(response, reverse('expense-list'))
        expense.refresh_from_db()
        self.assertEqual(expense.title, 'Updated Lunch')

    # =============================
    # ❌ Expense Delete View
    # =============================

    def test_delete_expense(self):
        """User can delete their expense."""
        expense = Expense.objects.first()
        response = self.client.post(reverse('expense-delete', args=[expense.id]))
        self.assertRedirects(response, reverse('expense-list'))
        self.assertFalse(Expense.objects.filter(id=expense.id).exists())

    # =============================
    # 🔢 Pagination
    # =============================

    def test_pagination_shows_ten_per_page(self):
        """ListView pagination should show 10 items per page."""
        # Create 15 expenses
        for i in range(15):
            Expense.objects.create(user=self.user, title=f'Expense {i}', amount=10, category='Misc')
        response = self.client.get(reverse('expense-list'))
        self.assertEqual(len(response.context['expenses']), 10)
