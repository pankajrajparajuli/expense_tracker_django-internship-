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
class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'

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
        return queryset

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

def dashboard(request):
    expenses = Expense.objects.all().order_by('-date')[:10]
    current_month = datetime.now().month

    total_monthly = Expense.objects.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0

    category_sums = Expense.objects.values('category').annotate(total=Sum('amount'))
    top_category = max(category_sums, key=lambda x: x['total'])['category'] if category_sums else 'N/A'

    # Pie Chart: category-wise
    category_data = {
        'data': [go.Pie(labels=[c['category'] for c in category_sums],
                        values=[c['total'] for c in category_sums],
                        marker=dict(colors=['#4a90e2','#50e3c2','#f5a623','#9013fe','#b8e986']))],
        'layout': go.Layout(margin=dict(t=20, b=20, l=20, r=20))
    }

    # Line Chart: expenses over time
    daily_expenses = (
        Expense.objects
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )

    trend_data = {
        'data': [go.Scatter(
            x=[d['date'] for d in daily_expenses],
            y=[d['total'] for d in daily_expenses],
            mode='lines+markers',
            line=dict(color='#4a90e2', width=2)
        )],
        'layout': go.Layout(margin=dict(t=20, b=40, l=40, r=20))
    }

    context = {
        'total_monthly': total_monthly,
        'top_category': top_category,
        'total_count': Expense.objects.count(),
        'recent_expenses': expenses,
        'category_data': json.dumps(category_data),
        'trend_data': json.dumps(trend_data),
    }

    return render(request, 'dashboard.html', context)


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