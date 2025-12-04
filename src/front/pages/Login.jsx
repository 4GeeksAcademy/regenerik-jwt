import React from 'react'
import { useState } from 'react';


const Login = ()=>{

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")


    const handleLogin = async () => {

        try {
            let response = await fetch("https://scaling-bassoon-74vwgjg4975hrj4p-3001.app.github.dev/api/token",{
                method:"POST",
                body: JSON.stringify({email:email,password:password}),
                headers:{
                    'Content-Type':'application/json'
                }
            })
            let data = await response.json()

            localStorage.setItem('access_token', data.access_token)
            console.log('El access token es : ',localStorage.getItem('access_token'))
            alert("Todo salio bien")

        } catch (error) {
            console.error(error)
        }
    }

    return(
        <div>
           <h1>Soy login</h1>
            <div className='m-5 bg-light'>
                <h2>Formulario de login:</h2>
                <br /><br />
                <h5>email:</h5>
                <input type="text" onChange={(e)=> setEmail(e.target.value)}/>
                <br />
                <br />
                <h5>password:</h5>
                <input type="password" onChange={(e)=> setPassword(e.target.value)}/>
                <br />
                <br />
                <button onClick={handleLogin}>Loguearse</button>
            </div>
        </div>
    )
}


export default Login;