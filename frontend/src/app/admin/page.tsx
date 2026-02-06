"use client";

import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

export default function Admin() {
  const [events, setEvents] = useState<any[]>([]);
  const [userId, setUserId] = useState("");
  const [boosts, setBoosts] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const [loadingEvents, setLoadingEvents] = useState(true);
  const [filter, setFilter] = useState("all");

  const loadEvents = async () => {
    setLoadingEvents(true);
    const r = await fetch(`${API}/events`);
    setEvents(await r.json());
    setLoadingEvents(false);
  };

  const loadBoosts = async () => {
    if (!userId) return;

    setLoading(true);
    const r = await fetch(
      `${API}/ml/debug-boosts?user_id=${userId}`
    );

    setBoosts(await r.json());
    setLoading(false);
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const filteredEvents = events.filter(e => 
    filter === "all" || e.event_type === filter
  );

  const eventCounts = {
    total: events.length,
    like: events.filter(e => e.event_type === "like").length,
    view: events.filter(e => e.event_type === "view").length,
    skip: events.filter(e => e.event_type === "skip").length,
  };

  const getEventIcon = (type: string) => {
    switch(type) {
      case "like": return "👍";
      case "view": return "👀";
      case "skip": return "⏭";
      default: return "📝";
    }
  };

  const getEventColor = (type: string) => {
    switch(type) {
      case "like": return "bg-green-500/10 border-green-500/30 text-green-400";
      case "view": return "bg-blue-500/10 border-blue-500/30 text-blue-400";
      case "skip": return "bg-gray-500/10 border-gray-500/30 text-gray-400";
      default: return "bg-purple-500/10 border-purple-500/30 text-purple-400";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white">
      
      {/* Ambient glow effect */}
      <div className="fixed top-0 right-1/4 w-[600px] h-[600px] bg-blue-600/5 rounded-full blur-[150px] pointer-events-none" />
      <div className="fixed bottom-0 left-1/4 w-[600px] h-[600px] bg-purple-600/5 rounded-full blur-[150px] pointer-events-none" />
      
      <div className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center gap-4 mb-3">
            <div className="w-14 h-14 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center text-3xl shadow-lg shadow-blue-600/30">
              🛠
            </div>
            <div>
              <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                Admin Dashboard
              </h1>
              <p className="text-slate-400 text-lg mt-1">
                System monitoring and analytics
              </p>
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-10">
          <div className="bg-gradient-to-br from-slate-800/60 to-slate-900/40 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm font-medium">Total Events</span>
              <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center text-xl">
                📊
              </div>
            </div>
            <div className="text-3xl font-bold text-white">{eventCounts.total}</div>
          </div>

          <div className="bg-gradient-to-br from-slate-800/60 to-slate-900/40 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm font-medium">Likes</span>
              <div className="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center text-xl">
                👍
              </div>
            </div>
            <div className="text-3xl font-bold text-green-400">{eventCounts.like}</div>
          </div>

          <div className="bg-gradient-to-br from-slate-800/60 to-slate-900/40 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm font-medium">Views</span>
              <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center text-xl">
                👀
              </div>
            </div>
            <div className="text-3xl font-bold text-blue-400">{eventCounts.view}</div>
          </div>

          <div className="bg-gradient-to-br from-slate-800/60 to-slate-900/40 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm font-medium">Skips</span>
              <div className="w-10 h-10 bg-gray-500/20 rounded-lg flex items-center justify-center text-xl">
                ⏭
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-400">{eventCounts.skip}</div>
          </div>
        </div>

        {/* Boost Checker Section */}
        <div className="mb-10 bg-gradient-to-br from-slate-800/60 to-slate-900/40 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8 shadow-2xl">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl flex items-center justify-center text-2xl shadow-lg shadow-purple-600/30">
              🔍
            </div>
            <div>
              <h2 className="text-2xl font-bold">Boost Analyzer</h2>
              <p className="text-slate-400 text-sm">Debug ML model boost scores for users</p>
            </div>
          </div>

          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <input
              placeholder="Enter User UUID (e.g., 550e8400-e29b-41d4-a716-446655440000)"
              className="flex-1 bg-slate-800/80 border border-slate-600/50 text-white px-5 py-4 rounded-xl focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/20 transition-all placeholder:text-slate-500"
              onChange={e => setUserId(e.target.value)}
              value={userId}
            />

            <button
              className="bg-gradient-to-r from-purple-600 to-pink-600 px-8 py-4 rounded-xl font-semibold hover:from-purple-500 hover:to-pink-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-purple-600/30 hover:shadow-purple-600/50 hover:scale-105 active:scale-100 flex items-center justify-center gap-2"
              onClick={loadBoosts}
              disabled={!userId || loading}
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Analyzing...
                </>
              ) : (
                <>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                  </svg>
                  Analyze Boosts
                </>
              )}
            </button>
          </div>

          {/* Boosts Display */}
          {Object.keys(boosts).length > 0 && (
            <div className="bg-slate-900/60 border border-slate-700/50 rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-300">Boost Analysis Results</h3>
                <span className="text-xs bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full">
                  User: {userId.substring(0, 8)}...
                </span>
              </div>
              <pre className="bg-slate-950/60 p-4 rounded-lg text-sm text-slate-300 overflow-x-auto border border-slate-700/30 font-mono">
                {JSON.stringify(boosts, null, 2)}
              </pre>
            </div>
          )}

          {Object.keys(boosts).length === 0 && userId && !loading && (
            <div className="bg-slate-900/40 border border-slate-700/30 rounded-xl p-8 text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-slate-800/50 rounded-full mb-4">
                <svg width="32" height="32" viewBox="0 0 20 20" fill="currentColor" className="text-slate-600">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <p className="text-slate-400">Enter a User UUID and click "Analyze Boosts" to see results</p>
            </div>
          )}
        </div>

        {/* Events Section */}
        <div className="bg-gradient-to-br from-slate-800/60 to-slate-900/40 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8 shadow-2xl">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-xl flex items-center justify-center text-2xl shadow-lg shadow-blue-600/30">
                📋
              </div>
              <div>
                <h2 className="text-2xl font-bold">Recent Events</h2>
                <p className="text-slate-400 text-sm">Real-time user activity stream</p>
              </div>
            </div>

            <button
              onClick={loadEvents}
              className="bg-slate-700/50 hover:bg-slate-600/50 px-4 py-2 rounded-lg transition-all flex items-center gap-2 text-sm font-medium border border-slate-600/30"
            >
              <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor" className={loadingEvents ? "animate-spin" : ""}>
                <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
              </svg>
              Refresh
            </button>
          </div>

          {/* Filter Tabs */}
          <div className="flex gap-2 mb-6 flex-wrap">
            {["all", "like", "view", "skip"].map(f => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${
                  filter === f
                    ? "bg-blue-600 text-white shadow-lg shadow-blue-600/30"
                    : "bg-slate-700/50 text-slate-300 hover:bg-slate-600/50 border border-slate-600/30"
                }`}
              >
                {f === "all" ? "All Events" : `${getEventIcon(f)} ${f.charAt(0).toUpperCase() + f.slice(1)}`}
                {f !== "all" && (
                  <span className="ml-2 bg-slate-900/50 px-2 py-0.5 rounded-full text-xs">
                    {eventCounts[f as keyof typeof eventCounts]}
                  </span>
                )}
              </button>
            ))}
          </div>

          {/* Events List */}
          {loadingEvents ? (
            <div className="flex items-center justify-center py-20">
              <svg className="animate-spin h-10 w-10 text-blue-500" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            </div>
          ) : filteredEvents.length > 0 ? (
            <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-slate-900">
              {filteredEvents.map((e, idx) => (
                <div
                  key={e.id || idx}
                  className={`border rounded-xl p-4 transition-all hover:scale-[1.01] ${getEventColor(e.event_type)}`}
                >
                  <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-4 flex-1 min-w-0">
                      <div className="text-2xl">{getEventIcon(e.event_type)}</div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-semibold capitalize">{e.event_type}</span>
                          <span className="text-xs bg-slate-900/50 px-2 py-0.5 rounded">
                            ID: {e.id}
                          </span>
                        </div>
                        
                        <div className="flex items-center gap-3 text-sm opacity-80 flex-wrap">
                          <span className="flex items-center gap-1">
                            <svg width="14" height="14" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                            </svg>
                            {e.user_id.substring(0, 8)}...
                          </span>
                          
                          <span className="flex items-center gap-1">
                            <svg width="14" height="14" viewBox="0 0 20 20" fill="currentColor">
                              <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" />
                            </svg>
                            Item {e.item_id}
                          </span>

                          {e.timestamp && (
                            <span className="flex items-center gap-1 text-xs">
                              <svg width="12" height="12" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                              </svg>
                              {new Date(e.timestamp).toLocaleString()}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-20">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-slate-800/50 rounded-full mb-4">
                <svg width="32" height="32" viewBox="0 0 20 20" fill="currentColor" className="text-slate-600">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-.464 5.535a1 1 0 10-1.415-1.414 3 3 0 01-4.242 0 1 1 0 00-1.415 1.414 5 5 0 007.072 0z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-slate-300">No events found</h3>
              <p className="text-slate-500">
                {filter === "all" 
                  ? "No user activity recorded yet" 
                  : `No ${filter} events found. Try a different filter.`}
              </p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}