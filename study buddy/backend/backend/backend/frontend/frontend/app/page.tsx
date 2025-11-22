"use client";

import {
  LiveKitRoom,
  RoomAudioRenderer,
  BarVisualizer,
  ControlBar,
  useConnectionState,
} from "@livekit/components-react";
import "@livekit/components-styles";
import { ConnectionState } from "livekit-client";
import { useEffect, useState } from "react";

export default function Home() {
  const [token, setToken] = useState("");
  
  // In a real app, fetch this from a backend API route
  useEffect(() => {
    (async () => {
      try {
        const resp = await fetch("/api/get-participant-token?room=falcon-room&username=user");
        const data = await resp.json();
        setToken(data.token);
      } catch (e) {
        console.error(e);
      }
    })();
  }, []);

  if (token === "") {
    return <div>Getting token...</div>;
  }

  return (
    <LiveKitRoom
      video={false}
      audio={true}
      token={token}
      serverUrl={process.env.NEXT_PUBLIC_LIVEKIT_URL}
      data-lk-theme="default"
      style={{ height: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}
    >
      <div className="flex flex-col items-center gap-4">
        <h1 className="text-2xl font-bold">Murf Falcon Agent</h1>
        <div className="h-32 w-64 bg-gray-900 rounded-lg flex items-center justify-center">
            <BarVisualizer state="state" barCount={5} trackRef={undefined} />
        </div>
        <ControlBar controls={{ camera: false, screenShare: false }} />
        <RoomAudioRenderer />
        <ConnectionStatus />
      </div>
    </LiveKitRoom>
  );
}

function ConnectionStatus() {
  const state = useConnectionState();
  return <div className="text-sm text-gray-500">Status: {state}</div>;
}