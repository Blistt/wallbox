"use client";
import Image from 'next/image';

export default function ImageGrid({ filenames }: { filenames: string[] }) {
  const imagePath = '/dataset/images/';

  return (
    <div className="grid grid-cols-3 gap-4 p-4">
      {filenames.map((filename, index) => (
        <div key={index} className="relative border border-gray-300 rounded-md overflow-hidden" style={{ width: '400px', height: '225px' }}>
          <Image 
            src={`${imagePath}${filename}`} 
            alt={`Image ${index + 1}`} 
            layout="fill" 
            objectFit="cover" 
          />
        </div>
      ))}
    </div>
  );
}
