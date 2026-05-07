import { useState } from "react";
import Upload from "./components/Upload";
import Chat from "./components/Chat";

function App() {
  const [fileId, setFileId] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [mediaType, setMediaType] = useState("");
  const [mediaUrl, setMediaUrl] = useState("");

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <div className="max-w-4xl mx-auto px-6 py-10">
        <div className="mb-10">
          <h1 className="text-5xl font-bold mb-3">AI Multimedia Q&A</h1>

          <p className="text-zinc-400">
            Upload PDFs or audio files and chat with AI.
          </p>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl">
          <Upload
            setFileId={setFileId}
            setAudioUrl={setMediaUrl}
            setMediaType={setMediaType}
            setMediaUrl={setMediaUrl}
          />

          {fileId && (
            <div className="mt-8">
              <Chat fileId={fileId} audioUrl={audioUrl} mediaType={mediaType} mediaUrl={mediaUrl} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
