import React, { useState, useRef, useEffect } from "react";

type ChatMessage = {
  sender: "user" | "bot";
  text: string;
  results?: Array<{ id: string; imageUrl?: string; description: string }>;
};

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages((msgs) => [...msgs, { sender: "user", text: input }]);
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      if (!res.ok) throw new Error("Fehler beim Chat-Request");
      const data = await res.json();
      setMessages((msgs) => [
        ...msgs,
        {
          sender: "bot",
          text: data.answer,
          results: data.results || [],
        },
      ]);
      setInput("");
    } catch (err: any) {
      setError(err.message || "Unbekannter Fehler");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 16, maxWidth: 500, margin: "0 auto", width: "100%" }}>
      <h1>Chat</h1>
      <div style={{ background: '#e9ecef', borderRadius: 8, padding: 12, marginBottom: 16, fontSize: 15, color: '#333', textAlign: 'left' }}>
        <b>Hinweis:</b> Hier kannst du einen <b>verlorenen Gegenstand</b> beschreiben. Gib möglichst viele Details an, damit passende Fundstücke gefunden werden können.
      </div>
      <div style={{ minHeight: 200, background: "#b0b0b0", borderRadius: 8, padding: 12, marginBottom: 16, overflowY: "auto", maxHeight: 300, width: "100%" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ marginBottom: 16, textAlign: msg.sender === "user" ? "right" : "left" }}>
            <div
              style={{
                display: "inline-block",
                background: msg.sender === "user" ? "#92aacd" : "#fff",
                color: msg.sender === "bot" ? "#222" : undefined,
                borderRadius: 8,
                padding: 8,
                maxWidth: "80%"
              }}
            >
              {msg.text}
            </div>
            {msg.sender === "bot" && msg.results && msg.results.length > 0 && (
              <div style={{ marginTop: 8 }}>
                <b>Trefferliste:</b>
                <div style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 8 }}>
                  {msg.results.map((item) => (
                    <div key={item.id} style={{ display: "flex", alignItems: "center", background: "#e9ecef", borderRadius: 8, padding: 8 }}>
                      {item.imageUrl && (
                        <img src={item.imageUrl} alt="Bild" style={{ width: 56, height: 56, objectFit: "cover", borderRadius: 6, marginRight: 12 }} />
                      )}
                      <div>
                        <div><b>ID:</b> {item.id}</div>
                        <div style={{ fontSize: 14 }}>{item.description}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <form onSubmit={sendMessage} style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Frage stellen oder nach einem Bild suchen..."
          style={{ flex: 1, minWidth: 0, padding: 10, fontSize: 16, borderRadius: 8, border: "1px solid #ccc" }}
          disabled={loading}
          aria-label="Chatnachricht eingeben"
        />
        <button type="submit" disabled={loading || !input.trim()} style={{ padding: "0 18px", fontSize: 16, borderRadius: 8 }}>
          Senden
        </button>
      </form>
      {error && <div style={{ color: "red", marginTop: 12 }}>{error}</div>}
    </div>
  );
};

export default Chat;
