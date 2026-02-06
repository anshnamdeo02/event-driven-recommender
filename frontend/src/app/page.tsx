"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getPoster } from "@/lib/tmdb";

const API = "http://127.0.0.1:8000";

export default function Home() {
  const router = useRouter();

  const [recs, setRecs] = useState<number[]>([]);
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const userId =
    typeof window !== "undefined"
      ? localStorage.getItem("user_id")
      : null;

  // ---------------- AUTH CHECK ----------------
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) router.push("/login");
  }, []);

  // ---------------- LOAD ITEMS + POSTERS ----------------
  useEffect(() => {
    fetch(`${API}/items`)
      .then(r => r.json())
      .then(async data => {
        const withPosters = await Promise.all(
          data.map(async (item: any) => ({
            ...item,
            poster: await getPoster(item.title)
          }))
        );

        setItems(withPosters);
      });
  }, []);

  // ---------------- LOAD RECS ----------------
  const loadRecs = async () => {
    if (!userId) return;

    setLoading(true);

    const r = await fetch(
      `${API}/ml/hybrid?user_id=${userId}`
    );

    const data = await r.json();

    setRecs(data.recommendations || []);
    setLoading(false);
  };

  // ---------------- EVENTS ----------------
  const sendEvent = async (itemId: number, type: string) => {
    if (!userId) return;

    await fetch(`${API}/events`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        item_id: itemId,
        event_type: type
      })
    });

    setRecs(prev => prev.filter(id => id !== itemId));
  };

  // ---------------- LOGOUT ----------------
  const logout = () => {
    localStorage.clear();
    router.push("/login");
  };

  // ---------------- UI ----------------
  return (
    <div className="min-h-screen bg-black text-white">

      {/* NAVBAR */}
      <div className="flex justify-between items-center px-10 py-6 border-b border-gray-800">
        <h1 className="text-4xl font-bold text-red-600">
          StreamFlix
        </h1>

        <button
          onClick={logout}
          className="bg-red-600 px-5 py-2 rounded hover:bg-red-700"
        >
          Logout
        </button>
      </div>

      {/* HERO */}
      <div className="px-10 py-12">
        <h2 className="text-3xl font-bold mb-2">
          Recommended For You
        </h2>

        <p className="text-gray-400 mb-6">
          Personalized picks based on your taste
        </p>

        <button
          onClick={loadRecs}
          className="bg-red-600 px-6 py-3 rounded hover:bg-red-700"
        >
          Get Recommendations
        </button>
      </div>

      {loading && (
        <p className="px-10 text-gray-400">Loading...</p>
      )}

      {/* MOVIE GRID */}
      <div className="px-10 pb-20 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">

        {recs.map((id: number) => {
          const item = items.find(i => i.id === id);

          return (
            <div
              key={id}
              className="bg-gray-900 rounded overflow-hidden hover:scale-105 transition"
            >
              {/* POSTER */}
              <img
                src={
                  item?.poster ||
                  "https://via.placeholder.com/300x450?text=Movie"
                }
                className="w-full h-[300px] object-cover"
              />

              {/* TITLE */}
              <div className="p-3">
                <h3 className="text-sm mb-3">
                  {item?.title || `Item ${id}`}
                </h3>

                {/* ACTIONS */}
                <div className="flex gap-2">
                  <button
                    onClick={() => sendEvent(id, "like")}
                    className="bg-green-600 px-3 py-1 rounded text-sm"
                  >
                    Like
                  </button>

                  <button
                    onClick={() => sendEvent(id, "view")}
                    className="bg-blue-600 px-3 py-1 rounded text-sm"
                  >
                    View
                  </button>

                  <button
                    onClick={() => sendEvent(id, "skip")}
                    className="bg-gray-600 px-3 py-1 rounded text-sm"
                  >
                    Skip
                  </button>
                </div>

              </div>
            </div>
          );
        })}

      </div>

    </div>
  );
}
