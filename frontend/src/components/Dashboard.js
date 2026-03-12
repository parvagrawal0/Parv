import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchNotes, deleteNote } from "../services/api";

const Dashboard = () => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadNotes = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await fetchNotes();
      setNotes(data.notes || data);
    } catch (err) {
      setError(err.response?.data?.message || "Failed to load notes");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadNotes();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this note?")) return;
    try {
      await deleteNote(id);
      setNotes((prev) => prev.filter((n) => n.id !== id));
    } catch (err) {
      setError(err.response?.data?.message || "Failed to delete note");
    }
  };

  return (
    <div>
      <div className="dashboard-header">
        <h2>Your Notes</h2>
        <Link to="/create" className="btn primary">
          + New Note
        </Link>
      </div>
      {error && <div className="error">{error}</div>}
      {loading ? (
        <p>Loading...</p>
      ) : notes.length === 0 ? (
        <p className="muted">No notes yet. Create your first note!</p>
      ) : (
        <div className="notes-grid">
          {notes.map((note) => (
            <div key={note.id} className="note-card">
              <h3>{note.title}</h3>
              <p className="note-content">{note.content}</p>
              <div className="note-actions">
                <Link className="btn-link" to={`/edit/${note.id}`}>
                  Edit
                </Link>
                <button
                  className="btn danger"
                  onClick={() => handleDelete(note.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;

