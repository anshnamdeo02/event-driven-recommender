"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const API = "http://127.0.0.1:8000";

export default function SignupPage() {
  const router = useRouter();

  const [email,setEmail]=useState("");
  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");
  const [msg,setMsg]=useState("");
  const [error,setError]=useState("");

  const signup = async (e:any)=>{
    e.preventDefault();
    setError("");
    setMsg("");

    const res = await fetch(`${API}/auth/signup`,{
      method:"POST",
      headers:{
        "Content-Type":"application/json"
      },
      body:JSON.stringify({
        email,
        username,
        password
      })
    });

    const data = await res.json();

    if(!res.ok){
      setError(
        typeof data.detail==="string"
          ? data.detail
          : JSON.stringify(data.detail)
      );
      return;
    }

    setMsg("Signup successful! Now login.");
  };

  return(
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <form onSubmit={signup} className="bg-neutral-900 p-8 rounded-xl w-80">
        <h1 className="text-2xl mb-6 text-center">Signup</h1>

        <input
          placeholder="Email"
          className="w-full p-3 mb-3 bg-neutral-800 rounded"
          value={email}
          onChange={e=>setEmail(e.target.value)}
          required
        />

        <input
          placeholder="Username"
          className="w-full p-3 mb-3 bg-neutral-800 rounded"
          value={username}
          onChange={e=>setUsername(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full p-3 mb-3 bg-neutral-800 rounded"
          value={password}
          onChange={e=>setPassword(e.target.value)}
          required
        />

        {error && <p className="text-red-500">{error}</p>}
        {msg && <p className="text-green-500">{msg}</p>}

        <button className="w-full bg-red-600 p-3 rounded mt-3">
          Signup
        </button>

        <p className="mt-4 text-sm text-center">
          Already have account?{" "}
          <span
            className="text-red-500 cursor-pointer"
            onClick={()=>router.push("/login")}
          >
            Login
          </span>
        </p>
      </form>
    </div>
  );
}
