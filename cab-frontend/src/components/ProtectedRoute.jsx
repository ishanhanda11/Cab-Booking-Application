import React from "react";
import { isAuthenticated } from "../api/auth";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/" />;
  }
  return children;
};

export default ProtectedRoute;
