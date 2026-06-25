import axios from "axios";
import { useState } from "react";
import API from "../api";

const Upload = ({ setFileId, setAudioUrl, setMediaType, setMediaUrl }) => {
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    let endpoint = "upload";

    if (file.type.includes("audio")) {
      endpoint = "upload-audio";
    }

    if (file.type.includes("video")) {
      endpoint = "upload-video";
    }

    try {
      const res = await API.post(`/${endpoint}`, formData);

      setFileId(res.data.file_id);
      const url = URL.createObjectURL(file);

      if (file.type.includes("audio") || file.type.includes("video")) {
        setAudioUrl(url);
        setMediaUrl(url);
      }

      if (file.type.includes("audio")) {
        setMediaType("audio");
      }

      if (file.type.includes("video")) {
        setMediaType("video");
      }
      alert("File uploaded successfully");
    } catch (err) {
      alert("Upload failed");
    }
    setLoading(false);
  };

  return (
    <div>
      <label className="block mb-3 text-lg font-semibold">Upload File</label>

      <input
        type="file"
        onChange={handleUpload}
        className="block w-full text-sm text-zinc-300
        file:mr-4 file:py-3 file:px-4
        file:rounded-xl file:border-0
        file:bg-white file:text-black
        hover:file:bg-zinc-300 cursor-pointer"
      />

      {loading && <p className="mt-4 text-zinc-400">Processing file...</p>}
    </div>
  );
};

export default Upload;
