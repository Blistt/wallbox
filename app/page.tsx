"use client";
import React, { useState } from 'react';
import UploadImage from './components/UploadImage';
import RetrieveImages from './components/RetrieveImages';
import ImageGrid from './components/ImageGrid';

interface ImageInfo {
  filename: string;
  url: string;
}

export default function Home() {
  const [images, setImages] = useState<ImageInfo[]>([]);

  const handleRetrieve = (retrievedImages: ImageInfo[]) => {
    console.log('handleRetrieve called with:', retrievedImages); // Debug log
    setImages(retrievedImages);
  };

  const handleUpload = () => {
    setImages([]);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="flex flex-col items-center space-y-8">
        <UploadImage onUpload={handleUpload} />
        <RetrieveImages onRetrieve={handleRetrieve} />
      </div>
      {images.length > 0 && (
        <div className="mt-8">
          <ImageGrid images={images} />
        </div>
      )}
    </main>
  );
}
