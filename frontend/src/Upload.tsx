import React, { useRef, useState } from "react";

type UploadResult = {
  id: string;
  imageUrl: string;
  description: string;
};

const Upload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<UploadResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [contact, setContact] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    setFile(f || null);
    setResult(null);
    setError(null);
    if (f) {
      setPreview(URL.createObjectURL(f));
    } else {
      setPreview(null);
    }
  };

  const handleCapture = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFileChange(e);
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !contact.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("image", file);
      formData.append("contact", contact);
      const res = await fetch("/items", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Upload fehlgeschlagen");
      const data = await res.json();
      setResult({
        id: data.id,
        imageUrl: data.imageUrl || preview || "",
        description: data.description,
      });
    } catch (err: any) {
      setError(err.message || "Unbekannter Fehler");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 16, maxWidth: 400, margin: "0 auto", width: "100%" }}>
      <h1>Upload</h1>
      <div style={{ background: '#e9ecef', borderRadius: 8, padding: 12, marginBottom: 16, fontSize: 15, color: '#333', textAlign: 'left' }}>
        <b>Hinweis:</b> Hier kannst du einen <b>gefundenen Gegenstand</b> als Bild einsenden. Bitte lade ein möglichst klares Foto hoch.<br/>
        Gib im Formular eine <b>Kontaktmöglichkeit</b> (z.B. E-Mail oder Telefonnummer) an, damit dich der/die Besitzer:in erreichen kann. Diese wird zusammen mit dem Bild gespeichert.
      </div>
      <form onSubmit={handleUpload} style={{ display: "flex", flexDirection: "column", gap: 16, width: "100%" }}>
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleCapture}
          style={{ marginBottom: 8 }}
          aria-label="Bild auswählen oder aufnehmen"
        />
        <input
          type="text"
          placeholder="Kontaktmöglichkeit (E-Mail oder Telefonnummer) *"
          value={contact}
          onChange={e => setContact(e.target.value)}
          style={{ padding: 10, fontSize: 15, borderRadius: 8, border: "1px solid #ccc" }}
          required
        />
        {preview && (
          <img src={preview} alt="Vorschau" style={{ width: "100%", borderRadius: 8, marginBottom: 8 }} />
        )}
        <button type="submit" disabled={!file || loading} style={{ padding: 12, fontSize: 16 }}>
          {loading ? "Hochladen..." : "Hochladen"}
        </button>
      </form>
      {error && <div style={{ color: "red", marginTop: 12 }}>{error}</div>}
      {result && (
        <div style={{ marginTop: 24, background: "#f5f5f5", borderRadius: 8, padding: 16, color: "#000" }}>
          <h3>Ergebnis</h3>
          <div><b>Item ID:</b> {result.id}</div>
          <img src={result.imageUrl} alt="Bildvorschau" style={{ width: "100%", borderRadius: 8, margin: "12px 0" }} />
          {/* Beschreibung wird nicht mehr angezeigt */}
        </div>
      )}
    </div>
  );
};

export default Upload;
