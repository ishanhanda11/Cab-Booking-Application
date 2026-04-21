from django.urls import path
from .views import RideView, AcceptRideView, CompleteRideView, AvailableRideView, DriverRidesView, CancelRideView, RideDetailsView, MyRideView, RatingView
urlpatterns = [
    path('create/', RideView.as_view(), name='create' ),
    path('<int:ride_id>/accept/', AcceptRideView.as_view(), name='accept'),
    path('<int:id>/complete/', CompleteRideView.as_view(), name='complete'),
    path('available/', AvailableRideView.as_view(), name='available'),
    path('my/', MyRideView.as_view(), name='myRide' ),
    path('driver/', DriverRidesView.as_view(), name='driver' ),
    path('<int:id>/cancel/', CancelRideView.as_view(), name='cancel'),
    path('details/<int:pk>/', RideDetailsView.as_view(), name='details'),
    path('rating/<int:id>/', RatingView.as_view(), name='rating' ),
]