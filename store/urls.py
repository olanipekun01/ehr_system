from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path('', views.index, name='index'),
    path('store/<str:pk>/', views.dept, name='dept_store'),
    path('stock/', views.newstock, name='newstock'),
    path('history/', views.history, name='dept_history'),
    path('history/<str:dept>/<str:item>/', views.history, name='item_history'),
    path('history/<str:dept>/', views.history, name='dept_item_history'),
    path('department/', views.department, name='department'),
    path('outofstock/', views.outOfStock, name='outofstock'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/<str:id>/', views.delete, name='delete'),
    path('removedepartment/<str:id>/', views.removeDept, name='removedepartment'),
    path('removesupplier/<str:id>/', views.removeSupp, name='removesupplier')
]
