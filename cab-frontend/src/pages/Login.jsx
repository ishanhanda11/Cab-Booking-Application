import React, { useState } from 'react'
import API from '../api/axios'
import { Navigate } from 'react-router-dom'
const Login = () => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const handleLogin= async()=>{
        try{

            const response = await API.post('accounts/login/',{
                email, password
            })
            console.log(response.data)
            localStorage.setItem('access', response.data.access)
            localStorage.setItem('role', response.data.role)
            window.location.href = '/dashboard/'
        } catch(error){
            console.log(error);
        }

    };
  return (
   <>
    <div>
        <div>
         <h2>Login</h2>
         <div>
            <label htmlFor="email">Email</label>
            <input type="email" name="email" id="email" onChange={(e)=>setEmail(e.target.value)}/>
         </div>
         <div>
            <label htmlFor="password">Password</label>
            <input type="text" id='password' onChange={(e)=>setPassword(e.target.value)} />
         </div>
         <button type="submit" onClick={handleLogin}>Login</button>
        </div>
       
    </div>
   </>
  )
}

export default Login