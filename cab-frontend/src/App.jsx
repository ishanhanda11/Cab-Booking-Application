import { useState } from "react";
import Login from "./pages/Login";
import { Router } from "react-router-dom";
import { Routes } from "react-router-dom";
import { Route } from "react-router-dom";
import SignUp from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import DriverDashboard from "./pages/DriverDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
const role = localStorage.getItem("role");
function App() {
  return (
    <>
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<SignUp />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              {role === "DRIVER" ? <DriverDashboard /> : <Dashboard />}
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}

export default App;
