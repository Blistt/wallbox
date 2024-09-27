"use client";

import React, { useState } from 'react';
import UploadImage from './components/UploadImage';
import RetrieveImages from './components/RetrieveImages';
import ImageGrid from './components/ImageGrid';

export default function Home() {
  const [imageUrls, setImageUrls] = useState<Record<string, string>>({});

  const handleRetrieve = (retrievedUrls: Record<string, string>) => {
    console.log('handleRetrieve called with:', retrievedUrls); // Debug log
    setImageUrls(retrievedUrls);
  };

  const handleUpload = () => {
    setImageUrls({});
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <UploadImage onUpload={handleUpload} />
        <RetrieveImages onRetrieve={handleRetrieve} />
      </div>
      {Object.keys(imageUrls).length > 0 && <ImageGrid imageUrls={imageUrls} />}
    </main>
  );
}