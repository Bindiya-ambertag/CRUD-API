from django.urls import path
from .views import employee_list, employee_detail


urlpatterns = [
    path('employees/', employee_list),
    path('employees/<str:id>/', employee_detail),

]
