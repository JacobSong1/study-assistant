import { useState } from "react"

function App() {
  const [notes, setNotes] = useState("")
  const [flashcards, setFlashcards] = useState([])
  const [loading, setLoading] = useState(false)
  const [flipped, setFlipped] = useState({})

  async function generate() {
    setLoading(true)
    const response = await fetch("http://study-assistant-production-fd84.up.railway.app/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notes }),
    })
    const data = await response.json()
    setFlashcards(data.flashcards)
    setFlipped({})
    setLoading(false)
  }

  async function uploadPDF(e) {
    const file = e.target.files[0]
    if (!file) return
    setLoading(true)
    const formData = new FormData()
    formData.append("file", file)
    const response = await fetch("http://study-assistant-production-fd84.up.railway.app/upload-pdf", {
      method: "POST",
      body: formData,
    })
    const data = await response.json()
    setFlashcards(data.flashcards)
    setFlipped({})
    setLoading(false)
  }

  function toggleFlip(i) {
    setFlipped(prev => ({ ...prev, [i]: !prev[i] }))
  }

  return (
    <div style={{ minHeight: "100vh", background: "#0f0f0f", color: "#f0f0f0", fontFamily: "sans-serif" }}>
      <div style={{ maxWidth: "680px", margin: "0 auto", padding: "60px 24px" }}>

        <div style={{ marginBottom: "48px", textAlign: "center" }}>
          <h1 style={{ fontSize: "36px", fontWeight: "700", margin: "0 0 8px", background: "linear-gradient(90deg, #a78bfa, #60a5fa)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
            Study With Shin
          </h1>
          <p style={{ color: "#ccc", margin: 0, fontSize: "15px" }}>Turn your notes into flashcards instantly.</p>
        </div>

        <div style={{ background: "#1a1a1a", borderRadius: "16px", padding: "24px", marginBottom: "16px", border: "1px solid #2a2a2a" }}>
          <p style={{ margin: "0 0 12px", fontSize: "13px", color: "#bbb", textTransform: "uppercase", letterSpacing: "0.08em" }}>Paste notes</p>
          <textarea
            rows={6}
            style={{ width: "100%", padding: "12px", fontSize: "15px", borderRadius: "10px", border: "1px solid #2a2a2a", background: "#111", color: "#f0f0f0", boxSizing: "border-box", resize: "vertical", outline: "none" }}
            placeholder="Paste your lecture notes here..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
          <button
            onClick={generate}
            disabled={loading || !notes.trim()}
            style={{ marginTop: "12px", padding: "12px 24px", fontSize: "15px", cursor: "pointer", background: "linear-gradient(90deg, #a78bfa, #60a5fa)", color: "white", border: "none", borderRadius: "10px", fontWeight: "600", width: "100%", opacity: loading || !notes.trim() ? 0.5 : 1 }}
          >
            {loading ? "Generating..." : "Generate Flashcards"}
          </button>
        </div>

        <div style={{ background: "#1a1a1a", borderRadius: "16px", padding: "24px", marginBottom: "40px", border: "1px solid #2a2a2a" }}>
          <p style={{ margin: "0 0 12px", fontSize: "13px", color: "#bbb", textTransform: "uppercase", letterSpacing: "0.08em" }}>Or upload a PDF</p>
          <input
            type="file"
            accept=".pdf"
            onChange={uploadPDF}
            style={{ fontSize: "14px", color: "#ccc" }}
          />
        </div>

        {loading && (
          <div style={{ textAlign: "center", color: "#666", padding: "40px 0" }}>
            Generating your flashcards...
          </div>
        )}

        {!loading && flashcards.length > 0 && (
          <div>
            <p style={{ fontSize: "13px", color: "#bbb", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "16px" }}>
              {flashcards.length} flashcards — click to flip
            </p>
            {flashcards.map((card, i) => (
              <div
                key={i}
                onClick={() => toggleFlip(i)}
                style={{
                  background: flipped[i] ? "#1e1b4b" : "#1a1a1a",
                  border: flipped[i] ? "1px solid #a78bfa" : "1px solid #2a2a2a",
                  borderRadius: "12px",
                  padding: "20px 24px",
                  marginBottom: "12px",
                  cursor: "pointer",
                  transition: "all 0.2s"
                }}
              >
                <p style={{ margin: "0 0 8px", fontSize: "11px", color: flipped[i] ? "#a78bfa" : "#999", textTransform: "uppercase", letterSpacing: "0.1em" }}>
                  {flipped[i] ? "Answer" : "Question"}
                </p>
                <p style={{ margin: 0, fontSize: "16px", lineHeight: "1.6", color: "#f0f0f0" }}>
                  {flipped[i] ? card.answer : card.question}
                </p>
              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  )
}

export default App