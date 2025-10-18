from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExpenseListView.as_view(), name='expense-list'),
    path('create/', views.ExpenseCreateView.as_view(), name='expense-create'),
    path('<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='expense-edit'),
    path('<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense-delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.custom_logout, name='custom_logout'),
]
