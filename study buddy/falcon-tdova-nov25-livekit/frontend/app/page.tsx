"use client";
import React, { useEffect, useState } from "react";
import { Room, connect } from "livekit-client";

export default function Page() {
  const [token, setToken] = useState<string | null>(null);
  const [status, setStatus] = useState("idle");

  useEffect(() => {
    async function fetchToken() {
      setStatus("fetching token");
      const res = await fetch("/api/token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identity: "guest-" + Math.floor(Math.random() * 10000) }),
      });
      const data = await res.json();
      setToken(data.token);
      setStatus("token ready");
    }
    fetchToken();
  }, []);

  async function join() {
    if (!token) return;
    setStatus("connecting");
    try {
      const url = process.env.NEXT_PUBLIC_LIVEKIT_URL || "ws://localhost:7880";
      const room = await connect(url, token);
      setStatus("connected");
      // Store room for further use - example only
      (window as any)._livekitRoom = room;
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error(err);
      setStatus("error");
    }
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>Murf Falcon Agent (Demo)</h1>
      <p>Status: {status}</p>
      {!token ? (
        <div>Getting token...</div>
      ) : (
        <button onClick={join}>Join LiveKit Room</button>
      )}
    </div>
  );
}
