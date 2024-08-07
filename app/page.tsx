"use client";
import React, { useState } from 'react';
import UploadImage from './components/UploadImage';
import RetrieveImages from './components/RetrieveImages';
import ImageGrid from './components/ImageGrid';

export default function Home() {
  const [filenames, setFilenames] = useState<string[]>([]);

  const handleRetrieve = (retrievedFilenames: string[]) => {
    setFilenames(retrievedFilenames);
  };

  const handleUpload = () => {
    setFilenames([]); // Clear the filenames state
  };

  return (
    <div className="flex flex-col items-center p-4 space-y-4">
      <UploadImage onUpload={handleUpload} />
      <RetrieveImages onRetrieve={handleRetrieve} />
      {filenames.length > 0 && <ImageGrid filenames={filenames} />}
    </div>
  );
}