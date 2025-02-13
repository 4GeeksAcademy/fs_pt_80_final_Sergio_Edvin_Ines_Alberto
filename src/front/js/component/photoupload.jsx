import React, { useState, useContext } from "react";
import "../../styles/photoupload.css";
import { Context } from "../store/appContext";

export const PhotoUpload = ({ onUploadSuccess }) => {
    const { actions } = useContext(Context);
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [uploadedUrl, setUploadedUrl] = useState('');

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            setPreviewUrl(URL.createObjectURL(file)); 
        }    
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert("Por favor, selecciona un archivo.");
            return;
        }

        setUploading(true);

        const imageUrl = await actions.uploadImageToBackend(selectedFile); 

        if (imageUrl) {
            setUploadedUrl(imageUrl);
            alert("Foto subida con éxito ✨ ");
            onUploadSuccess(imageUrl);
            setPreviewUrl(imageUrl);
        } else {
            alert("Error al subir la foto 📢");
        }
        setUploading(false);
    };

    return (
        <div className="photo-upload">
            <label htmlFor="photo-input" className="__image__">
                {previewUrl ? (
                    <img src={previewUrl} alt="Vista previa" className="__preview_image__" />
                ) : (
                    <span className="fa-solid fa-plus"></span>
                )}
            </label>
            <input
                type="file"
                className="photo-input"
                id="photo-input"
                onChange={handleFileChange}
            />
            <button
                onClick={handleUpload}
                className="btn btn-color mt-3"
                disabled={uploading || !selectedFile}
            >
                {uploading ? "Subiendo..." : "Subir Foto"}
            </button>
        </div>
    );
};