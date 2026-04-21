import React, { useState } from "react";
import API from "../api/axios";
const SignUp = () => {
  const [form, setForm] = useState({
    email: "",
    name: "",
    phone: "",
    password: "",
    role: "PASSENGER",
  });

  const handleSignUp = async () => {
    try {
      const response = await API.post("accounts/register/", form);
      alert("signUp succesffuly");
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <>
      <div>
        <div>
          <h1>Sign Up</h1>
          <div>
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              onChange={(e) => {
                setForm({ ...form, email: e.target.value });
              }}
            />
          </div>
          <div>
            <label htmlFor="name">Name</label>
            <input
              type="name"
              id="name"
              onChange={(e) => {
                setForm({ ...form, name: e.target.value });
              }}
            />
          </div>
          <div>
            <label htmlFor="phone">Phone Number</label>
            <input
              type="text"
              id="phone"
              onChange={(e) => {
                setForm({ ...form, phone: e.target.value });
              }}
            />
          </div>
          <div>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              onChange={(e) => {
                setForm({ ...form, password: e.target.value });
              }}
            />
          </div>
          <select onChange={(e) => setForm({ ...form, role: e.target.value })}>
            <option value="PASSENGER">Passenger</option>
            <option value="DRIVER">Driver</option>
          </select>
          <button type="submit" onClick={handleSignUp}>Submit</button>
        </div>
      </div>
    </>
  );
};

export default SignUp;
