import { useState } from "react";
import API from "../api";

const Upload = ({ onUploadSuccess }) => {
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    let endpoint = "upload";
    if (file.type.includes("audio")) endpoint = "upload-audio";
    if (file.type.includes("video")) endpoint = "upload-video";

    try {
      const res = await API.post(`/${endpoint}`, formData);
      alert("Analysis complete!");
      onUploadSuccess(res.data.file_id);
    } catch (err) {
      alert(err.response?.data?.detail || "Asset pipeline ingestion failure");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-2 px-2">
      <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider">
        Add Document / Media
      </label>
      <input
        type="file"
        onChange={handleUpload}
        disabled={loading}
        className="block w-full text-xs text-zinc-400
        file:mr-3 file:py-2 file:px-3
        file:rounded-xl file:border-0
        file:bg-white file:text-black
        file:font-medium hover:file:bg-zinc-300 cursor-pointer disabled:opacity-50"
      />
      {loading && <p className="text-xs text-zinc-400 animate-pulse mt-1">Processing file...</p>}
    </div>
  );
};

export default Upload;