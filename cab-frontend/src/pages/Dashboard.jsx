import React, { useEffect, useState } from "react";
import API from "../api/axios";
const Dashboard = () => {
  const [rides, setRides] = useState([]);
  const role = localStorage.getItem("role");
  const [pickUp, setPickUp] = useState("");
  const [drop, setDrop] = useState("");
  const [rating, setRating] = useState("");
  const fetchRides = async () => {
    try {
      let url = role === "PASSENGER" ? "rides/my/" : "rides/";
      const response = await API.get(url);
      setRides(response.data);
      console.log(response.data);
    } catch (error) {
      console.log(error);
    }
  };
  const CreateRide = async () => {
    try {
      const response = await API.post("rides/create/", {
        pickup_location: pickUp,
        drop_location: drop,
      });
      console.log(response);
      fetchRides();
    } catch (error) {
      console.log(error);
    }
  };
  const cancelRide = async (id) => {
    try {
      const response = await API.post(`rides/${id}/cancel/`);
      console.log(response.data);
      fetchRides();
    } catch (error) {
      console.log(error);
    }
  };
  const submitRating = async (id) => {
    try {
      const response = await API.post(`rides/rating/${id}/`, {
        rating: Number(rating),
      });
    } catch (error) {}
  };
  useEffect(() => {
    fetchRides();
  }, []);
  return (
    <>
      <div className="container mt-4">
        {/* Header */}
        <h1 className="mb-4">Dashboard</h1>

        {/* Ride List */}
        <div className="row">
          {rides.map((ride) => (
            <div key={ride.id} className="col-md-6 mb-3">
              <div className="card shadow-sm">
                <div className="card-body">
                  <p>
                    <strong>{ride.pickup_location}</strong> →{" "}
                    <strong>{ride.drop_location}</strong>
                  </p>

                  <p>
                    Status:{" "}
                    <span
                      className={`badge ${
                        ride.status === "COMPLETED"
                          ? "bg-success"
                          : ride.status === "CANCELLED"
                            ? "bg-danger"
                            : "bg-warning text-dark"
                      }`}
                    >
                      {ride.status}
                    </span>
                  </p>

                  <p className="fw-bold text-success">Fare: ₹{ride.fare}</p>

                  <p className="text-muted">
                    {role === "PASSENGER"
                      ? `Driver: ${ride.driver}`
                      : `Passenger: ${ride.passenger}`}
                  </p>
                  {ride.status === 'COMPLETED' && ride.rating_by_passenger != null &&(
                    <p className="text-muted">Rating: {ride.rating_by_passenger}</p>
                  )}

                  {/* Cancel Button */}
                  {ride.status !== "COMPLETED" &&
                    ride.status !== "CANCELLED" && (
                      <button
                        className="btn btn-outline-danger mb-3"
                        onClick={() => cancelRide(ride.id)}
                      >
                        Cancel Ride
                      </button>
                    )}

                  {/* Rating Section */}
                  {ride.status === "COMPLETED" && !ride.rating_by_passenger &&(
                    <div className="mt-3">
                      <h6>Give Rating</h6>

                      <div className="d-flex gap-2">
                        <input
                          type="number"
                          min="1"
                          max="5"
                          placeholder="1-5"
                          className="form-control"
                          style={{ maxWidth: "100px" }}
                          onChange={(e) => setRating(e.target.value)}
                        />
                        
                        <button
                          className="btn btn-primary"
                          onClick={() => submitRating(ride.id)}
                        >
                          Submit
                        </button>
                      </div>

                      <hr />
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Create Ride (Passenger Only) */}
        {role === "PASSENGER" && (
          <div className="card mt-5 shadow-sm">
            <div className="card-body">
              <h4 className="mb-3">Create Ride</h4>

              <div className="mb-3">
                <label className="form-label">Pick Up Location</label>
                <input
                  type="text"
                  className="form-control"
                  onChange={(e) => setPickUp(e.target.value)}
                />
              </div>

              <div className="mb-3">
                <label className="form-label">Drop Location</label>
                <input
                  type="text"
                  className="form-control"
                  onChange={(e) => setDrop(e.target.value)}
                />
              </div>

              <button className="btn btn-success w-100" onClick={CreateRide}>
                Submit Ride
              </button>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default Dashboard;
