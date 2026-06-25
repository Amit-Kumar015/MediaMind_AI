import { useState, useRef, useEffect } from "react";
import API from "../api";

const Chat = ({ chatDetails, setChatDetails }) => {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const mediaRef = useRef(null);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatDetails?.messages]);

  const token = localStorage.getItem("token");
  const mediaType = chatDetails.type || (chatDetails.title?.includes(".pdf") ? "pdf" : "audio"); 
  const mediaUrl = `http://127.0.0.1:8000/media/${chatDetails.file_id}?token=${token}`;

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    const currentQuestion = question;
    setQuestion("");

    setChatDetails((prev) => ({
      ...prev,
      messages: [...prev.messages, { role: "user", content: currentQuestion, timestamp: null }],
    }));

    try {
      const res = await API.post("/chat", {
        chat_id: chatDetails.chat_id,
        question: currentQuestion,
      });

      setChatDetails((prev) => ({
        ...prev,
        messages: [
          ...prev.messages,
          { role: "assistant", content: res.data.answer, timestamp: res.data.timestamp },
        ],
      }));
    } catch (err) {
      alert("Error getting response from model");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full max-w-4xl mx-auto px-6 py-6">
      <div className="border-b border-zinc-800 pb-4 mb-4">
        <h2 className="text-lg font-bold truncate">{chatDetails.title}</h2>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {chatDetails.messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[85%] rounded-2xl p-4 border text-base leading-relaxed ${
              msg.role === "user"
                ? "bg-zinc-800 border-zinc-700 ml-auto text-zinc-100"
                : "bg-zinc-900 border-zinc-800 mr-auto text-zinc-300"
            }`}
          >
            <p className="font-semibold text-xs text-zinc-400 uppercase tracking-wider mb-1">
              {msg.role === "user" ? "You" : "MediaMind AI"}
            </p>
            <p className="whitespace-pre-wrap">{msg.content}</p>

            {(mediaType === "audio" || mediaType === "video") && msg.timestamp !== null && msg.timestamp !== undefined && (
              <button
                onClick={() => {
                  if (mediaRef.current) {
                    mediaRef.current.currentTime = msg.timestamp;
                    mediaRef.current.play();
                  }
                }}
                className="mt-3 block bg-zinc-800 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 px-3 py-1.5 rounded-lg text-xs font-medium"
              >
                ▶ Jump to {msg.timestamp}s
              </button>
            )}
          </div>
        ))}
        {loading && (
          <div className="bg-zinc-900 border border-zinc-800 text-zinc-400 mr-auto max-w-[85%] rounded-2xl p-4 text-sm animate-pulse">
            Thinking...
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      {mediaType === "audio" && (
        <div className="mt-4">
          <audio controls ref={mediaRef} src={mediaUrl} className="w-full max-h-10" />
        </div>
      )}

      {mediaType === "video" && (
        <div className="mt-4">
          <video
            controls
            ref={mediaRef}
            src={mediaUrl}
            className="w-full max-h-64 bg-black rounded-xl shadow-inner"
          />
        </div>
      )}

      <div className="flex gap-3 mt-2 pt-2 bg-zinc-950">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && askQuestion()}
          placeholder="Ask something about this resource..."
          className="flex-1 bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 text-sm outline-none focus:border-zinc-700 text-white placeholder-zinc-500"
        />
        <button
          onClick={askQuestion}
          className="bg-white text-black px-5 rounded-xl font-semibold text-sm hover:bg-zinc-300 transition cursor-pointer"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;