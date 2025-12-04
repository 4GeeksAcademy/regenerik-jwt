import React from 'react'
import { useState } from 'react';

const Register = () => {

    const [ email, setEmail ] = useState("")
    const [ password ,setPassword] = useState("")

    const handleRegister = async () => {
        let payload = {
            email: email,
            password: password,
            is_active: true
        }

        try {
            let response = await fetch("https://scaling-bassoon-74vwgjg4975hrj4p-3001.app.github.dev/api/users",{
                method:"POST",
                body: JSON.stringify(payload),
                headers:{
                    'Content-Type': 'application/json'
                }
            })

            let data = await response.json()
            alert("Esta es la data: " + JSON.stringify(data))

        } catch (error) {
            console.error(error)
        }
    }

    return(
        <div>
            <h1>Soy registro</h1>
            <div className='m-5 bg-light'>
                <h2>Formulario de registro:</h2>
                <br /><br />
                <h5>email:</h5>
                <input type="text" onChange={(e)=> setEmail(e.target.value)}/>
                <br />
                <br />
                <h5>password:</h5>
                <input type="password" onChange={(e)=> setPassword(e.target.value)}/>
                <br />
                <br />
                <button onClick={handleRegister}>Registrarse</button>
            </div>
        </div>
    )
}

export default Register;