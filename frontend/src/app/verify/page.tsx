"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const API="http://127.0.0.1:8000";

export default function VerifyPage(){
  const router=useRouter();

  const[email,setEmail]=useState("");
  const[otp,setOtp]=useState("");
  const[error,setError]=useState("");

  const handleVerify=async()=>{
    setError("");

    const res=await fetch(`${API}/auth/verify`,{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({email,otp})
    });

    const data=await res.json();

    if(!res.ok){
      setError(data.detail||"Invalid OTP");
      return;
    }

    alert("Verified!");
    router.push("/login");
  };

  return(
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <div className="w-full max-w-md bg-neutral-900 p-8 rounded-xl">
        <h1 className="text-3xl mb-6 text-center">Verify OTP</h1>

        <input
          placeholder="Email"
          className="w-full p-3 mb-3 bg-neutral-800 rounded"
          value={email}
          onChange={e=>setEmail(e.target.value)}
        />

        <input
          placeholder="OTP"
          className="w-full p-3 mb-3 bg-neutral-800 rounded"
          value={otp}
          onChange={e=>setOtp(e.target.value)}
        />

        {error&&<p className="text-red-500">{error}</p>}

        <button
          onClick={handleVerify}
          className="w-full bg-red-600 p-3 rounded"
        >
          Verify
        </button>
      </div>
    </div>
  );
}
