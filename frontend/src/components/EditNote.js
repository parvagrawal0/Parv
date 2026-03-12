import React, { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { fetchNoteById, updateNote } from "../services/api";

const EditNote = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [formData, setFormData] = useState({ title: "", content: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const loadNote = async () => {
      setError("");
      try {
        const data = await fetchNoteById(id);
        setFormData({ title: data.title, content: data.content });
      } catch (err) {
        setError(err.response?.data?.message || "Failed to load note");
      } finally {
        setLoading(false);
      }
    };
    loadNote();
  }, [id]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      await updateNote(id, formData);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.message || "Failed to update note");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="card">
      <h2>Edit Note</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit} className="form">
        <label>
          Title
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Content
          <textarea
            name="content"
            value={formData.content}
            onChange={handleChange}
            rows={5}
            required
          />
        </label>
        <div className="form-actions">
          <button className="btn" type="button" onClick={() => navigate("/")}>
            Cancel
          </button>
          <button className="btn primary" type="submit" disabled={saving}>
            {saving ? "Saving..." : "Update"}
          </button>
        </div>
      </form>
      <p className="muted">
        <Link to="/">Back to Dashboard</Link>
      </p>
    </div>
  );
};

export default EditNote;

