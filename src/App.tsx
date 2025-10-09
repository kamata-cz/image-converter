import { useState, useRef } from 'react';
import './App.css';
import { ImageConverter } from './components/ImageConverter';

interface ImageFile {
  file: File;
  preview: string;
  width: number;
  height: number;
}

function App() {
  const [imageFiles, setImageFiles] = useState<ImageFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files).filter((file) =>
      file.type.startsWith('image/')
    );

    await processFiles(files);
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      await processFiles(files);
    }
  };

  const processFiles = async (files: File[]) => {
    const imagePromises = files.map(
      (file) =>
        new Promise<ImageFile>((resolve) => {
          const reader = new FileReader();
          reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
              resolve({
                file,
                preview: e.target?.result as string,
                width: img.width,
                height: img.height,
              });
            };
            img.src = e.target?.result as string;
          };
          reader.readAsDataURL(file);
        })
    );

    const newImages = await Promise.all(imagePromises);
    setImageFiles((prev) => [...prev, ...newImages]);
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const removeImage = (index: number) => {
    setImageFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Image Converter</h1>
          <p className="text-gray-600">
            Convert, resize, and compress your images in the browser
          </p>
        </header>

        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-4 border-dashed rounded-lg p-12 text-center transition-colors ${
            isDragging
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 bg-white hover:border-gray-400'
          }`}
        >
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
            aria-hidden="true"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <div className="mt-4">
            <button
              onClick={handleButtonClick}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Select Images
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              onChange={handleFileSelect}
              className="hidden"
            />
          </div>
          <p className="mt-2 text-sm text-gray-600">or drag and drop images here</p>
          <p className="mt-1 text-xs text-gray-500">
            Supports: JPEG, PNG, WebP, AVIF, GIF, SVG
          </p>
        </div>

        {imageFiles.length > 0 && (
          <>
            <div className="mt-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                Loaded Images ({imageFiles.length})
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {imageFiles.map((img, index) => (
                  <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
                    <div className="relative aspect-video bg-gray-200">
                      <img
                        src={img.preview}
                        alt={img.file.name}
                        className="w-full h-full object-contain"
                      />
                      <button
                        onClick={() => removeImage(index)}
                        className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition-colors"
                        aria-label="Remove image"
                      >
                        ×
                      </button>
                    </div>
                    <div className="p-4">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {img.file.name}
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        {img.width} × {img.height} • {(img.file.size / 1024).toFixed(1)} KB
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <ImageConverter images={imageFiles} />
          </>
        )}
      </div>
    </div>
  );
}

export default App;
