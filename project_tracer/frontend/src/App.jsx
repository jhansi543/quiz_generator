import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

function Message({ m }) {
  if (m.type === "system") return null;
  const isUser = m.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div
        className={`max-w-[75%] p-3 rounded-lg ${
          isUser
            ? "bg-gradient-to-br from-indigo-500 to-purple-600 text-white"
            : "bg-gray-800 text-gray-100"
        }`}>
        {m.title && <div className="text-xs text-gray-300 mb-1">{m.title}</div>}
        <div className="whitespace-pre-wrap">{m.text}</div>
      </div>
    </div>
  );
}

export default function App() {
  // Base URL for backend API. Use Vite env var VITE_API_BASE in production
  // e.g. VITE_API_BASE=https://jhansi-six.vercel.app
  const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8003";

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi — paste a Wikipedia article URL and I will generate a short quiz.",
      type: "assistant",
    },
  ]);
  const [history, setHistory] = useState([]);
  const [selectedHistoryId, setSelectedHistoryId] = useState(null);
  const [error, setError] = useState(null);
  const listRef = useRef(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    // auto-scroll
    if (listRef.current)
      listRef.current.scrollTop = listRef.current.scrollHeight;
  }, [messages]);

  async function fetchHistory() {
    try {
      const res = await axios.get(`${API_BASE}/history`);
      setHistory(res.data || []);
      setError(null);
    } catch (e) {
      console.error("Failed to fetch history:", e);
      setError(e.response?.data || e.message || "Failed to fetch history");
    }
  }

  async function handleSend() {
    if (!input) return;
    const url = input.trim();
    setError(null);
    const userMsg = { role: "user", text: url };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/generate_quiz`, {
        url,
      });
      const data = res.data;
      // format quiz into readable text
      let text = "";
      if (data.title) text += `Title: ${data.title}\n\n`;
      if (data.quiz && data.quiz.length) {
        text += data.quiz
          .map((q, idx) => {
            return `${idx + 1}. ${q.question}\nOptions: ${q.options?.join(
              " | "
            )}\nAnswer: ${q.answer}\nExplanation: ${q.explanation}\n`;
          })
          .join("\n");
      } else {
        text += "No quiz returned.";
      }
      const assistantMsg = { role: "assistant", text, title: data.title };
      setMessages((m) => [...m, assistantMsg]);
      // refresh history
      fetchHistory();
    } catch (e) {
      const msg = e.response?.data || e.message;
      setError(msg);
      setMessages((m) => [
        ...m,
        { role: "assistant", text: `Error: ${JSON.stringify(msg)}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function loadHistoryItem(id) {
    try {
  const res = await axios.get(`${API_BASE}/quiz/${id}`);
      const data = res.data;
      // Build assistant messages: first the extracted article text, then the quiz
      const fullText = data.full_text || data.fullText || "";
      const intro = fullText ? `Extracted article text:\n\n${fullText}` : "";
      const quizText =
        data.quiz
          ?.map(
            (q, idx) =>
              `${idx + 1}. ${q.question}\nOptions: ${q.options?.join(
                " | "
              )}\nAnswer: ${q.answer}\n`
          )
          .join("\n") || "No quiz";

      // Replace the current messages with the selected history item (not append)
      const newMessages = [];
      if (intro)
        newMessages.push({ role: "assistant", text: intro, title: data.title });
      newMessages.push({
        role: "assistant",
        text: quizText,
        title: data.title,
      });
      setMessages(newMessages);
      setSelectedHistoryId(id);
      // refresh history list (in case of external changes)
      fetchHistory();
    } catch (e) {
      setError(e.response?.data || e.message);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-indigo-900 to-purple-900 text-gray-100">
      <div className="w-full h-screen p-6 grid grid-cols-12 gap-6">
        <div className="col-span-3 bg-gray-800/60 rounded-lg p-4 h-full flex flex-col min-h-0">
          <h2 className="text-lg font-semibold mb-3">History</h2>
          <div className="space-y-2 overflow-auto scrollbar-thin flex-1 min-h-0">
            {history.length === 0 && (
              <div className="text-sm text-gray-400">No history yet.</div>
            )}
            {history.map((h) => (
              <button
                key={h.id}
                onClick={() => loadHistoryItem(h.id)}
                className={`w-full text-left p-2 rounded hover:bg-indigo-700/40 ${
                  selectedHistoryId === h.id ? "bg-indigo-700/60" : ""
                }`}>
                <div className="font-medium">{h.title}</div>
                <div className="text-xs text-gray-400">{h.url}</div>
                <div className="text-xs text-gray-500">{h.date_generated}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="col-span-9 bg-gradient-to-b from-gray-800/80 via-gray-900/80 to-black/80 rounded-lg p-4 flex flex-col h-full min-h-0">
          <div
            className="flex-1 overflow-auto scrollbar-thin p-2 min-h-0"
            ref={listRef}>
            {messages.map((m, i) => (
              <Message key={i} m={m} />
            ))}
          </div>

          <div className="flex-none sticky bottom-0 bg-gradient-to-b from-transparent to-black/40 pt-2">
            <div className="flex gap-2 items-center">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Paste Wikipedia URL and press Enter"
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleSend();
                }}
                className="flex-1 rounded px-3 py-2 bg-gray-700 text-gray-100 border border-gray-700"
              />
              <button
                onClick={handleSend}
                disabled={loading || !input}
                className="px-4 py-2 rounded bg-gradient-to-br from-indigo-500 to-purple-600 text-white">
                {loading ? "Generating..." : "Send"}
              </button>
            </div>
            {error && (
              <div className="mt-2 text-red-400 text-sm">
                {JSON.stringify(error)}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
