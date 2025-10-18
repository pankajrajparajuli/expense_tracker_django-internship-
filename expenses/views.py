import json
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Expense
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.contrib.auth import logout
from datetime import datetime
from plotly import graph_objs as go
import plotly
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10  # ✅ show 10 per page

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)
        category = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if category and category != "All":
            queryset = queryset.filter(category=category)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expenses = self.get_queryset()
        total = expenses.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        context['total_amount'] = total
        context['categories'] = Expense.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', 'All')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['title', 'amount', 'category']
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.amount <= 0:
            messages.error(self.request, "Amount must be greater than 0.")
            return self.form_invalid(form)
        messages.success(self.request, "Expense added successfully.")
        return super().form_valid(form)

class ExpenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Expense
    fields = ['title', 'amount', 'category']
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense-list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Expense updated successfully.")
        return super().form_valid(form)

class ExpenseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Expense deleted successfully.")
        return super().delete(request, *args, **kwargs)


@login_required
def dashboard(request):
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('-date')[:10]
    current_month = datetime.now().month

    # === Monthly total ===
    total_monthly = (
        Expense.objects
        .filter(user=user, date__month=current_month)
        .aggregate(Sum('amount'))['amount__sum'] or 0
    )

    # === Category breakdown (Pie Chart) ===
    category_sums = (
        Expense.objects
        .filter(user=user)
        .values('category')
        .annotate(total=Sum('amount'))
    )
    top_category = max(category_sums, key=lambda x: x['total'])['category'] if category_sums else 'N/A'

    pie = go.Figure(
        data=[go.Pie(
            labels=[c['category'] for c in category_sums],
            values=[c['total'] for c in category_sums],
            hole=0.4
        )]
    )
    pie.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    # === DAILY Expenses (non-cumulative) ===
    daily_expenses = (
        Expense.objects
        .filter(user=user)
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )

    line_daily = go.Figure(
        data=[go.Scatter(
            x=[d['date'].strftime('%d %b') for d in daily_expenses],
            y=[d['total'] for d in daily_expenses],
            mode='lines+markers',
            line=dict(color='#4a90e2', width=3),
            marker=dict(size=7),
            name="Daily Spending"
        )]
    )
    line_daily.update_layout(
        yaxis_title="Amount (Rs)",
        xaxis_title="Day",
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode="x unified"
    )

    # === WEEKLY Expenses ===
    # Compute ISO week and sum per week
    weekly_expenses = (
        Expense.objects
        .filter(user=user)
        .extra(select={'week': "strftime('%%W', date)"})  # for SQLite; for PostgreSQL: Extract(week from date)
        .values('week')
        .annotate(total=Sum('amount'))
        .order_by('week')
    )

    line_weekly = go.Figure(
        data=[go.Scatter(
            x=[f"Week {int(d['week'])}" for d in weekly_expenses],
            y=[d['total'] for d in weekly_expenses],
            mode='lines+markers',
            line=dict(color='#50e3c2', width=3),
            marker=dict(size=7),
            name="Weekly Spending"
        )]
    )
    line_weekly.update_layout(
        yaxis_title="Amount (Rs)",
        xaxis_title="Week Number",
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode="x unified"
    )

    # === Convert to JSON for frontend ===
    category_data = json.dumps(pie, cls=plotly.utils.PlotlyJSONEncoder)
    trend_daily = json.dumps(line_daily, cls=plotly.utils.PlotlyJSONEncoder)
    trend_weekly = json.dumps(line_weekly, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        'total_monthly': total_monthly,
        'top_category': top_category,
        'total_count': expenses.count(),
        'recent_expenses': expenses,
        'category_data': category_data,
        'trend_daily': trend_daily,
        'trend_weekly': trend_weekly,
    }

    return render(request, 'expenses/dashboard.html', context)


def custom_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})