from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User, Course, Employee, Department
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email','name','role','password','phone']

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
class CustomTokenSerialzier(TokenObtainPairSerializer):
    username_field = 'email'
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('User doesnt exist')
        data = super().validate(attrs)
        data['email'] = user.email
        data['role'] = user.role
        return data

class ProductSerailizer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    category = serializers.ChoiceField(choices=['electronics','clothing','food'])
    password = serializers.CharField(write_only=True)
    discounted_price = serializers.SerializerMethodField()

    def get_discounted_price(self,obj):
       return round(float(obj['price']) * 0.9, 2)

class BookingSerailizer(serializers.Serializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    guests = serializers.IntegerField()
    promocode = serializers.CharField(required=False)

    def validate_guests(self,value):
        if value < 1:
           raise serializers.ValidationError('guests can not be less than 1')
        elif value > 10:
            raise serializers.ValidationError('guests cannot be more than 10')
        return value
    
    def validate_promocode(self, value):
        if not value.startswith('SAVE'):
            raise serializers.ValidationError('promo code must start with save')
        return value



    def validate(self, data):
        if data['check_in'] > data['check_out']:
            raise serializers.ValidationError('check in data cannot be greater than check out date')
        return data

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only':True},
            'created_at':{'read_only':True},
            'secret_code':{'write_only': True}
        }
    def create(self,validated_data):
        free = validated_data.get('is_free')
        if free == True:
            validated_data['price'] = 0
        course = Course(**validated_data)
        course.save()
        return course

class DepartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Department
        fields = ['id','name','location']
        extra_kwargs = {
            'id':{'read_only':True}
        }
        
class EmployeeSeriailzer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = Employee
        fields = '__all__'

class DetailDepartmentSerializer(serializers.ModelSerializer):
    employees = EmployeeSeriailzer(many=True, read_only=True)
    class Meta:
        model = Department
        fields = '__all__'
       

