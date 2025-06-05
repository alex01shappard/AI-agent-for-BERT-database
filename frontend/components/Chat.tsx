"use client";

import React, { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";

export default function Chat() {
  const [messages, setMessages] = useState<{ from: "user" | "bot"; text: string }[]>([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { from: "user", text: input }]);
    setInput("");

    try {
      const res = await fetch("http://localhost:8000/check_prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
      });
      const data = await res.json();

      setMessages((prev) => [...prev, { from: "bot", text: data.answer || "Нет ответа" }]);
    } catch (error) {
      setMessages((prev) => [...prev, { from: "bot", text: "Ошибка при запросе к серверу" }]);
    }
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 bg-opacity-90 flex items-center justify-center px-4">
      <div className="w-full max-w-xl h-[600px] bg-white bg-opacity-10 backdrop-blur-md rounded-2xl shadow-xl border border-white border-opacity-20 flex flex-col">
        <header className="px-6 py-4 border-b border-white border-opacity-20 text-white text-xl font-semibold select-none">
          AI-Chat
        </header>

        <main className="flex-1 overflow-y-auto px-6 py-4 space-y-4 text-white">
          {messages.length === 0 && (
            <p className="text-gray-300 text-center mt-20 select-none">
              Введите запрос внизу, чтобы начать общение
            </p>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.from === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[70%] px-4 py-2 rounded-lg whitespace-pre-wrap ${
                  msg.from === "user"
                    ? "bg-blue-600 bg-opacity-90 text-white rounded-br-none shadow-md"
                    : "bg-white bg-opacity-30 text-gray-900 rounded-bl-none shadow-md"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}

          <div ref={messagesEndRef} />
        </main>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            sendMessage();
          }}
          className="px-4 py-3 border-t border-white border-opacity-20 flex gap-3 items-center"
        >
          <textarea
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Введите сообщение..."
            className="resize-none flex-1 rounded-md border border-white border-opacity-20 bg-gray-800 bg-opacity-70 placeholder-gray-300 text-white px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition"
          />

          <button
            type="submit"
            aria-label="Отправить сообщение"
            className="bg-blue-600 bg-opacity-70 hover:bg-opacity-90 active:bg-opacity-100 transition-colors rounded-md p-2 flex items-center justify-center shadow-lg"
          >
            <Send className="w-5 h-5 text-white" />
          </button>
        </form>
      </div>
    </div>
  );
}
