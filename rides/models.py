from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.
class Ride(models.Model):
     STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
     passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
     driver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='drives' )
     pickup_location = models.CharField(max_length=255)
     drop_location = models.CharField(max_length=255)
     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
     fare = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
     distance = models.FloatField(null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f"{self.passenger} - {self.status}"
     

class Rating(models.Model):
     ride = models.OneToOneField(Ride, on_delete=models.CASCADE)
     passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
     driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
     rating_by_passenger = models.IntegerField(null=True, blank=True)
     rating_by_driver = models.IntegerField(null=True, blank=True)

     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return f"Rating for Ride {self.ride.id}"