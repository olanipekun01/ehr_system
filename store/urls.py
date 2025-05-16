from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path('', views.index, name='index'),
    path('store/<str:pk>/', views.dept, name='dept_store'),
    path('stock/', views.newstock, name='newstock'),
    path('history/', views.history, name='dept_history'),
    # path('history/<str:dept>/<str:item>/', views.history, name='item_history'),
    # path('history/<str:dept>/', views.history, name='dept_item_history'),
    path('department/', views.department, name='department'),
    path('outofstock/', views.outOfStock, name='outofstock'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('units/', views.units, name='units'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/<str:id>/', views.delete, name='delete'),
    # path('removedepartment/<str:id>/', views.removeDept, name='removedepartment'),
    path('removesupplier/<str:id>/', views.removeSupp, name='removesupplier'),
    path('removeunit/<str:id>/', views.removeUnit, name='removeunit'),

    path('updateunit/', views.updateUnit, name='updateunit'),
    path('inventory/', views.inventory, name='inventory'),
    path('add-to-cart/<str:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('updatestock/', views.updateStock, name='updatestock'),
    # path('report', views.report, name='report')
]
