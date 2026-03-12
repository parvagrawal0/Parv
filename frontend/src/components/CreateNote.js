import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { createNote } from "../services/api";

const CreateNote = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ title: "", content: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await createNote(formData);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.message || "Failed to create note");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Create Note</h2>
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
          <button className="btn primary" type="submit" disabled={loading}>
            {loading ? "Saving..." : "Save"}
          </button>
        </div>
      </form>
      <p className="muted">
        <Link to="/">Back to Dashboard</Link>
      </p>
    </div>
  );
};

export default CreateNote;

