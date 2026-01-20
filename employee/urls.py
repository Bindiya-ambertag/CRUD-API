# from django.urls import path
# from .views import employee_list, employee_detail
#
#
# urlpatterns = [
#     path('employees/', employee_list),
#     path('employees/<str:id>/', employee_detail),
#
# ]
from django.urls import path
from .views import EmployeeListView, EmployeeDetailView

urlpatterns = [
    path('employees/', EmployeeListView.as_view()),
    path('employees/<str:id>/', EmployeeDetailView.as_view()),
]
