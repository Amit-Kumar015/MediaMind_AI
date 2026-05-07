import { useState, useRef } from "react";
import axios from "axios";

const Chat = ({ fileId, audioUrl, mediaType, mediaUrl }) => {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const audioRef = useRef(null);

  const askQuestion = async () => {
    if (!question) return;

    setLoading(true);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        {},
        {
          params: {
            file_id: fileId,
            question,
          },
        },
      );

      setMessages((prev) => [
        ...prev,
        {
          question,
          answer: res.data.answer,
          timestamp: res.data.timestamp,
        },
      ]);

      setQuestion("");
    } catch (err) {
      alert("Error getting answer");
    }

    setLoading(false);
  };

  return (
    <div className="">
      <div className="mt-4 space-y-6 max-h-96 overflow-y-auto">
        {messages.map((msg, i) => (
          <div
            key={i}
            className="bg-zinc-800 border border-zinc-700 rounded-2xl p-5"
          >
            <p className="font-semibold mb-2">Q: {msg.question}</p>

            <p className="text-zinc-300 whitespace-pre-wrap">{msg.answer}</p>

            <button
              onClick={() => {
                if (audioRef.current) {
                  audioRef.current.currentTime = msg.timestamp;
                  audioRef.current.play();
                }
              }}
              className="mt-4 bg-zinc-700 hover:bg-zinc-600 px-4 py-2 rounded-lg text-sm"
            >
              ▶ Jump to {msg.timestamp.toFixed(2)}s
            </button>
          </div>
        ))}
      </div>

      {loading && <p className="mt-4 text-zinc-400">Thinking...</p>}

      {audioUrl && mediaType === "audio" && (
        <audio controls ref={audioRef} src={audioUrl} className="w-full mt-6" />
      )}

      {mediaUrl && mediaType === "video" && (
        <video
          controls
          ref={audioRef}
          src={mediaUrl}
          className="w-full mt-6 rounded-xl"
        />
      )}

      <div className="flex gap-3 mt-6">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something..."
          className="flex-1 bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 outline-none"
        />

        <button
          onClick={askQuestion}
          className="bg-white text-black px-6 rounded-xl font-semibold hover:bg-zinc-300"
        >
          Ask
        </button>
      </div>
    </div>
  );
};

export default Chat;
