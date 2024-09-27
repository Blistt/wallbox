import React from 'react';
import Image from 'next/image';

export default function ImageGrid({ imageUrls }: { imageUrls: Record<string, string> }) {
  return (
    <div className="grid grid-cols-3 gap-4 p-4">
      {Object.entries(imageUrls).map(([filename, url], index) => (
        <div key={index} className="relative border border-gray-300 rounded-md overflow-hidden" style={{ width: '400px', height: '225px' }}>
          <Image 
            src={url} 
            alt={`Image ${filename}`} 
            layout="fill" 
            objectFit="cover" 
          />
        </div>
      ))}
    </div>
  );
}
