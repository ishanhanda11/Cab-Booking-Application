from rest_framework import serializers
from .models import User
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email','name','role','password','phone']

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

