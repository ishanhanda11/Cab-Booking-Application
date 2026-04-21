from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ProductView, BookView, CourseView, DepartmentView, EmployeeView
urlpatterns = [
    path('register/',RegisterView.as_view(), name='register' ),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('students/',ProductView.as_view()),
    path('booking/', BookView.as_view()),
    path('course/', CourseView.as_view()),
    path('department/',DepartmentView.as_view()),
    path('employee/',EmployeeView.as_view()),
]