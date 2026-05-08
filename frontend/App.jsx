import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const uploadVideo = async () => {
    if (!file) return;

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(
        `http://localhost:8000/upload/?query=${encodeURIComponent(query)}`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await res.json();
      console.log("FULL RESPONSE:", data);

      if (data.route === "clarification") {
        setMessages((prev) => [
          ...prev,
          { role: "user", content: query },
          { role: "assistant", content: data.message },
        ]);

        setSuggestions(data.suggestions || []);
        setQuery("");
        setLoading(false);
        return;
      }

      setSuggestions([]);

  
      let assistantText = "";

      if (data.route === "transcription") {
        assistantText = data.result;
      } else if (data.route === "vision") {
        assistantText =
          "Detected objects: " +
          (data.result.objects?.join(", ") || "none");
      } else if (data.route === "generation") {
        assistantText =
          data.result.message +
          "\nPDF: http://localhost:8000/download/" +
          data.result.file;
      } else {
        assistantText = JSON.stringify(data.result);
      }

      setMessages((prev) => [
        ...prev,
        { role: "user", content: query },
        { role: "assistant", content: assistantText },
      ]);
      setQuery("");
    } catch (err) {
      console.error("Upload failed:", err);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error: " + err.message },
      ]);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Video AI App</h1>

      {/* FILE UPLOAD */}
      <input
        type="file"
        accept="video/mp4"
        onChange={(e) => setFile(e.target.files[0])}
      />

      {/* QUERY INPUT */}
      <div style={{ marginTop: 10 }}>
        <input
          type="text"
          placeholder="Ask something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ width: 300 }}
        />

        <button onClick={uploadVideo} disabled={!file || loading}>
          {loading ? "Processing..." : "Send"}
        </button>
      </div>

      {/* CHAT MESSAGES */}
      <div style={{ marginTop: 20 }}>
        {messages.map((msg, i) => (
          <p key={i}>
            <b>{msg.role}:</b> {msg.content}
          </p>
        ))}
      </div>

      {/* SUGGESTION BUTTONS */}
      {suggestions.length > 0 && (
        <div style={{ marginTop: 10 }}>
          <p><b>Did you mean:</b></p>

          {suggestions.map((s, i) => (
            <button
              key={i}
              onClick={() => {
                setQuery(s);
                setSuggestions([]);
              }}
              style={{
                marginRight: 8,
                marginTop: 5,
                padding: "8px 12px",
                cursor: "pointer",
              }}
            >
              {s}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;