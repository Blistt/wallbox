"use client";
import { useState } from 'react';

export default function RetrieveImagesButton({ onRetrieve }: { onRetrieve: (filenames: string[]) => void }) {
  const handleRetrieve = async () => {
    const response = await fetch('http://127.0.0.1:5328/api/retrieve_images', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query_path: 'public/uploaded_images/',
        image_embedding_path: 'public/dataset/images',
      }),
    });

    if (response.ok) {
      const data = await response.json();
      onRetrieve(data.retrieved_images);
    } else {
      console.error('Error retrieving images');
    }
  };

  return (
    <button 
      onClick={handleRetrieve} 
      className="px-4 py-2 text-white rounded-md transition-colors duration-300 bg-gradient-to-r from-purple-500 to-blue-950 hover:from-pink-300 hover:to-purple-500"
    >
      Retrieve Similar Images
    </button>
  );
  
}
