from django.shortcuts import render
from .serializers import RideSerializer, RatingSerializer
from .models import Ride, Rating
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .permissions import IsDriver, IsPassenger
from django.db import transaction
from django.db.models import Q
# Create your views here.
class RideView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RideSerializer

    def perform_create(self, serializer):
        if self.request.user.role != 'PASSENGER':
            raise PermissionDenied("Only passengers can create rides")
     
        pickup = self.request.data.get('pickup_location')
        drop = self.request.data.get('drop_location')
        distance = len(pickup) + len(drop)
        base_fare = 50
        price_per_km = 10
        fare = base_fare + (distance * price_per_km)
        user = self.request.user
        serializer.save(passenger = user, distance = distance, fare=fare,)


class AcceptRideView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self,request, ride_id):
        try:
            ride = Ride.objects.select_for_update().get(id=ride_id)
        except Ride.DoesNotExist:
             return Response({"error": "Ride not found"}, status=404)
        
        # if request.user.role != 'DRIVER':
        #      return Response({"error": "Only drivers can accept rides"}, status=403)
        
        if ride.status != 'PENDING':
             return Response({"error": "Ride already accepted"}, status=400)
        
        active_ride = Ride.objects.filter(driver=request.user, status='ACCEPTED').exists()
        if active_ride:
            return Response(
            {"error": "You already have an active ride"},
            status=400
            )   
        
        ride.driver = request.user
        ride.status = 'ACCEPTED'
        ride.save()
        return Response({"message": "Ride accepted"})
    
class CompleteRideView(APIView):
    permission_classes = [IsAuthenticated, IsDriver]
    def post(self, request, id):
        try:
            ride = Ride.objects.get(id=id)
        except Ride.DoesNotExist:
            return Response("eror: Ride is not found", status=404)
        
        
        if request.user != ride.driver:
            return Response('You dont have the permission to complete the ride', status=403)
        
        if ride.status != 'ACCEPTED':
            return Response('error: "ride is not in progress" ', status=400)
        
        ride.status = 'COMPLETED'
        ride.save()
        return Response({"message": "Ride completed successfully"})
    
class AvailableRideView(generics.ListAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated, IsDriver]
    
    def get_queryset(self):
        return Ride.objects.filter(status='PENDING', driver__isnull = True)

class MyRideView(generics.ListAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ride.objects.filter(passenger = self.request.user)
    
class DriverRidesView(generics.ListAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ride.objects.filter(driver = self.request.user)
    

class CancelRideView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,id):
        try:
            ride = Ride.objects.get(id=id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=404)
        
        if ride.passenger != request.user:
            return Response({"error": "Not your ride"}, status=403)
        
        if ride.status == 'COMPLETED':
            return Response({"error": "Cannot cancel completed ride"}, status=400)
        
        ride.status = 'CANCELLED'
        ride.save()
        return Response({"message": "Ride cancelled"})


class RideDetailsView(generics.RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        ride = super().get_object()
        user = self.request.user

        if ride.passenger != user and ride.driver != user:
            raise PermissionDenied('YOU ARE NOT ALLOWED TO VIEW THIS!!!') 

        return ride
    

class RatingView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self,request,id):
        try:
            ride = Ride.objects.select_for_update().get(id=id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=404)
        
        if request.user != ride.passenger and request.user != ride.driver:
            return Response({"error": "Not allowed"}, status=403)

        if ride.status != 'COMPLETED':
            return Response({"error": "Ride not completed yet"}, status=400)
        
        rating_obj, created = Rating.objects.get_or_create(
            ride=ride,
            passenger=ride.passenger,
            driver=ride.driver
        )
        if request.user == ride.passenger and rating_obj.rating_by_passenger:
            return Response({"error": "You already rated"}, status=400)
        if request.user == ride.driver and rating_obj.rating_by_driver:
            return Response({"error": "You already rated"}, status=400)
        # Passenger rating driver
        if request.user == ride.passenger:
            if rating_obj.rating_by_passenger is not None:
                return Response({"error": "Already rated"}, status=400)
            rating_obj.rating_by_passenger = request.data.get("rating")

        # Driver rating passenger
        elif request.user == ride.driver:
            if rating_obj.rating_by_driver is not None:
                return Response({"error": "Already rated"}, status=400)
            rating_obj.rating_by_driver = request.data.get("rating")

        rating_obj.save()

        return Response({"message": "Rating submitted"})