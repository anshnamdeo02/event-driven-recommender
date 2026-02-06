"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const API = "http://127.0.0.1:8000";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const login = async (e:any) => {
    e.preventDefault();
    setError("");

    const body = new URLSearchParams();
    body.append("username", email); // OAuth expects username
    body.append("password", password);

    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body,
    });

    const data = await res.json();

    if (!res.ok) {
      setError(
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail)
      );
      return;
    }

    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user_id", data.user_id);
    router.push("/");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <form onSubmit={login} className="bg-neutral-900 p-8 rounded-xl w-80">
        <h1 className="text-2xl mb-6 text-center">Login</h1>

        <input
          type="email"
          placeholder="Email"
          className="w-full p-3 mb-3 bg-neutral-800 rounded"
          value={email}
          onChange={e=>setEmail(e.target.value)}
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

        {error && (
          <p className="text-red-500 mb-3 text-sm">
            {error}
          </p>
        )}

        <button
          type="submit"
          className="w-full bg-red-600 p-3 rounded hover:bg-red-500"
        >
          Login
        </button>

        <p className="mt-4 text-sm text-center">
          No account?{" "}
          <span
            className="text-red-500 cursor-pointer"
            onClick={()=>router.push("/signup")}
          >
            Signup
          </span>
        </p>
      </form>
    </div>
  );
}
