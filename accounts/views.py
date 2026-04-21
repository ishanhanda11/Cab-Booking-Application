from django.shortcuts import render
from rest_framework import generics
from .models import User, Course, Department, Employee
from .serializers import RegisterSerializer, CustomTokenSerialzier, ProductSerailizer, BookingSerailizer, CourseSerializer, DepartmentSerializer, EmployeeSeriailzer, DetailDepartmentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerialzier
    permission_classes = [AllowAny]

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        return Response({
            'email': user.email,
            'role': user.role,
            'name': user.name
        })

class ProductView(APIView):
    def post(self,request):
        product1 = {
            'name':'ishan handa',
            'description': 'this is the description baby',
            'price': 10.5,
            'category':'electronics',
            'password':'ishan789',
            
        }
        serializer = ProductSerailizer(data=product1)
        if serializer.is_valid():
            output = ProductSerailizer(serializer.validated_data)
            return Response(output.data)
        else:
            return Response(serializer.errors)
        
class BookView(APIView):
    def post(self,request):
        book = {
            'check_in': '2022-11-8',
            'check_out': '2022-11-9',
            'guests': 8,
            
        }
        serialzer = BookingSerailizer(data=book)
        if serialzer.is_valid():
            return Response(serialzer.validated_data)
        else:
            return Response(serialzer.errors)
        
class CourseView(APIView):
    def post(self,request):
        course = Course.objects.all()
        serializer = CourseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class DepartmentView(APIView):
    def get(self,request):
        deparments = Department.objects.all()
        serializer = DetailDepartmentSerializer(deparments, many=True)
        return Response(serializer.data)


class EmployeeView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSeriailzer(employees, many=True)
        return Response(serializer.data)