import React, { useState } from 'react';

interface ImageInfo {
  filename: string;
  url: string;
  order: number;
}

export default function RetrieveImagesButton({ onRetrieve }: { onRetrieve: (images: ImageInfo[]) => void }) {
  const [isLoading, setIsLoading] = useState(false);

  const handleRetrieve = async () => {
    console.log('Button clicked'); // Debug log
    setIsLoading(true);
    try {
      console.log('Sending request to server'); // Debug log
      const response = await fetch('http://127.0.0.1:5328/api/retrieve_images', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query_path: 'public/uploaded_images/',
          image_embedding_path: 'public/dataset/embeddings/23',
        }),
      });
      console.log('Received response from server'); // Debug log
      if (response.ok) {
        const data = await response.json();
        console.log('Retrieved data:', data); // Debug log
        
        // Sort the images based on the 'order' field
        const sortedImages = data.images.sort((a: ImageInfo, b: ImageInfo) => a.order - b.order);
        
        console.log('Sorted images:', sortedImages.map((img: ImageInfo) => img.filename)); // Debug log
        
        onRetrieve(sortedImages);
      } else {
        console.error('Error retrieving images');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button 
      onClick={handleRetrieve} 
      className="px-4 py-2 text-white rounded-md transition-colors duration-300 bg-gradient-to-r 
                from-purple-500 to-blue-950 hover:from-pink-300 hover:to-purple-500"
      disabled={isLoading}
    >
      {isLoading ? 'Retrieving...' : 'Retrieve Similar Images'}
    </button>
  );
}