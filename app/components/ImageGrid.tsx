import React from 'react';
import Image from 'next/image';

interface ImageInfo {
  filename: string;
  url: string;
}

export default function ImageGrid({ images }: { images: ImageInfo[] }) {
  return (
    <div className="grid grid-cols-3 gap-4 p-4">
      {images.map((image, index) => (
        <div key={index} className="relative border border-gray-300 rounded-md overflow-hidden" style={{ width: '400px', height: '225px' }}>
          <Image
            src={image.url}
            alt={`Image ${image.filename}`}
            layout="fill"
            objectFit="cover"
          />
        </div>
      ))}
    </div>
  );
}