import React, { useEffect, useState } from "react";
import API from "../api/axios";
const DriverDashboard = () => {
  const [rides, setRides] = useState([]);
  const [myRides, setMyRides] = useState([]);
  const [rideDetails, setRideDetails] = useState(null);
  const AvailableRides = async () => {
    try {
      const response = await API.get("rides/available/");
      const res = await API.get("rides/driver/");
      console.log(response.data);
      setRides(response.data);
      setMyRides(res.data);
    } catch (error) {
      console.log(error);
    }
  };
  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("role");
    window.location.href = "/";
  };
  const AcceptRide = async (id) => {
    try {
      const response = await API.post(`rides/${id}/accept/`);
      AvailableRides();
    } catch (error) {
      console.log(error);
    }
  };
  const viewDetails = async (id) => {
    try {
      const response = await API.get(`rides/details/${id}/`);
      console.log(response.data);
      setRideDetails(response.data);
    } catch (error) {
      console.log(error);
    }
  };
  const CompleteRide = async (id) => {
    try {
      const response = await API.post(`rides/${id}/complete/`);
      AvailableRides();
    } catch (error) {
      console.log(error);
    }
  };
  useEffect(() => {
    AvailableRides();
  }, []);
  return (
    <>
      <div className="container mt-4">
        {/* Header */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h1 className="h3">Driver Dashboard</h1>
          <button className="btn btn-danger" onClick={logout}>
            Logout
          </button>
        </div>

        {/* Available Rides */}
        <h4 className="mb-3">Available Rides</h4>
        <div className="row">
          {rides.map((ride) => (
            <div key={ride.id} className="col-md-4 mb-3">
              <div className="card shadow-sm">
                <div className="card-body">
                  <p className="card-text">
                    <strong>{ride.pickup_location}</strong> →{" "}
                    <strong>{ride.drop_location}</strong>
                  </p>
                  <p className="text-success fw-bold">Fare: ₹{ride.fare}</p>

                  <button
                    className="btn btn-primary w-100"
                    onClick={() => AcceptRide(ride.id)}
                  >
                    Accept Ride
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Current Ride */}
        <h4 className="mt-5 mb-3">Current Ride</h4>
        <div className="row">
          {myRides.map((ride) => (
            <div key={ride.id} className="col-md-6 mb-3">
              <div className="card border-warning shadow-sm">
                <div className="card-body">
                  <p>
                    <strong>{ride.pickup_location}</strong> →{" "}
                    <strong>{ride.drop_location}</strong>
                  </p>
                  <p>
                    Status:{" "}
                    <span className="badge bg-warning text-dark">
                      {ride.status}
                    </span>
                  </p>

                  {ride.status !== "COMPLETED" && (
                    <div className="d-flex gap-2">
                      <button
                        className="btn btn-success"
                        onClick={() => CompleteRide(ride.id)}
                      >
                        Complete
                      </button>
                      <button
                        className="btn btn-outline-secondary"
                        onClick={() => viewDetails(ride.id)}
                      >
                        View Details
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default DriverDashboard;
