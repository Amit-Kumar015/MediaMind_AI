import { useState, useEffect } from "react";
import Upload from "./components/Upload";
import Chat from "./components/Chat";
import Auth from "./components/Auth";
import API from "./api";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [chats, setChats] = useState([]);
  const [activeChatId, setActiveChatId] = useState("");
  const [activeChatDetails, setActiveChatDetails] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
      fetchChats();
    }
  }, [isAuthenticated]);

  const fetchChats = async () => {
    try {
      const res = await API.get("/chats");
      setChats(res.data);
    } catch (err) {
      console.error("Failed to load chat histories");
    }
  };

  const createNewChat = async (fileId) => {
    try {
      const res = await API.post("/chat/new", { file_id: fileId });
      setChats((prev) => [res.data, ...prev]);
      handleSelectChat(res.data.chat_id);
    } catch (err) {
      alert("Failed to initiate a new conversation thread");
    }
  };

  const handleSelectChat = async (chatId) => {
    try {
      setActiveChatId(chatId);
      const res = await API.get(`/chat/${chatId}`);
      setActiveChatDetails(res.data);
    } catch (err) {
      alert("Error pulling discussion logs");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
    setActiveChatId("");
    setActiveChatDetails(null);
  };

  if (!isAuthenticated) {
    return <Auth onAuthSuccess={() => setIsAuthenticated(true)} />;
  }

  return (
    <div className="flex h-screen bg-zinc-950 text-white overflow-hidden">
      <aside className="w-64 bg-zinc-900 border-r border-zinc-800 flex flex-col justify-between h-full">
        <div className="p-4 overflow-y-auto flex-1 space-y-6">
          <div>
            <h2 className="text-xl font-bold tracking-tight mb-4">MediaMind AI</h2>
            <Upload onUploadSuccess={(fileId) => createNewChat(fileId)} />
          </div>

          <div className="space-y-2">
            <h3 className="text-xs font-semibold text-zinc-300 uppercase tracking-wider px-2">
              Recent Conversations
            </h3>
            <div className="space-y-1">
              {chats.map((c) => (
                <button
                  key={c.chat_id}
                  onClick={() => handleSelectChat(c.chat_id)}
                  className={`w-full text-left px-3 py-2 text-sm rounded-xl block truncate transition ${
                    activeChatId === c.chat_id
                      ? "bg-zinc-800 text-white font-medium"
                      : "text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-200"
                  }`}
                >
                  💬 {c.title}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="p-4 border-t border-zinc-800">
          <button
            onClick={handleLogout}
            className="w-full bg-red-500 hover:bg-red-600 text-gray-50 border border-zinc-700 py-2 rounded-xl text-sm transition cursor-pointer"
          >
            Sign Out
          </button>
        </div>
      </aside>

      <main className="flex-1 flex flex-col bg-zinc-950 h-full relative">
        {activeChatDetails ? (
          <Chat 
            chatDetails={activeChatDetails} 
            setChatDetails={setActiveChatDetails}
          />
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
            <div className="max-w-md space-y-2">
              <h1 className="text-3xl font-bold">Your Intelligence Space</h1>
              <p className="text-zinc-400 text-sm">
                Upload a primary asset file or select a persistent conversation thread from your historical log to interact with the model context.
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;