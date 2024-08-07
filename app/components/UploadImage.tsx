"use client";
import { useState } from 'react';
import Image from 'next/image';

export default function UploadImage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    const response = await fetch('/routes', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      setResultImage(data.filePath);
    } else {
      console.error('Error uploading image');
    }
  };

  return (
    <div className="flex flex-col items-center p-4 space-y-4">
      <h1 className="text-2xl font-bold">Upload Image</h1>
      <form onSubmit={handleSubmit} className="flex flex-col items-center space-y-4">
        <input 
          type="file" 
          onChange={handleFileChange} 
          className="px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:ring-blue-200"
        />
        <button 
          type="submit" 
          className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-900 transition-colors duration-300"
        >
          Upload
        </button>
      </form>
      {resultImage && (
        <div className="mt-4">
          <h2 className="text-xl font-semibold">Uploaded Image:</h2>
          <Image 
            src={resultImage} 
            alt="Uploaded" 
            width={500} 
            height={500} 
            className="mt-2 border border-gray-300 rounded-md"
          />
        </div>
      )}
    </div>
  );
}