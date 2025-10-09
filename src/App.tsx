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

  const clearAll = () => {
    setImageFiles([]);
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <header className="mb-10 text-center animate-fadeIn">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
            <span className="inline-block">Image</span>{' '}
            <span className="inline-block bg-white text-transparent bg-clip-text">Converter</span>
          </h1>
          <p className="text-white/90 text-lg md:text-xl max-w-2xl mx-auto">
            Convert, resize, and compress your images instantly in the browser.
            No uploads, no waiting, complete privacy.
          </p>
        </header>

        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            glass rounded-2xl p-8 md:p-12 text-center transition-all duration-300
            file-input-area ${isDragging ? 'dragging scale-105 border-white/50' : 'border-white/20'}
            ${isDragging ? 'shadow-2xl' : 'shadow-xl hover:shadow-2xl'}
          `}
        >
          <div className="relative">
            <svg
              className={`mx-auto h-16 w-16 md:h-20 md:w-20 transition-all duration-300 ${
                isDragging ? 'text-purple-600 scale-110' : 'text-purple-500'
              }`}
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

            <div className="mt-6 space-y-4">
              <button
                onClick={handleButtonClick}
                className="btn-gradient text-white px-8 py-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform transition-all duration-300"
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

              <p className="text-gray-700 font-medium">or drag and drop images here</p>
              <p className="text-sm text-gray-600">
                Supports: JPEG, PNG, WebP, AVIF, GIF, SVG
              </p>
            </div>
          </div>
        </div>

        {imageFiles.length > 0 && (
          <>
            <div className="mt-10 animate-fadeIn">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl md:text-3xl font-bold text-white">
                  Loaded Images ({imageFiles.length})
                </h2>
                <button
                  onClick={clearAll}
                  className="text-white/80 hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-white/10"
                >
                  Clear All
                </button>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {imageFiles.map((img, index) => (
                  <div
                    key={index}
                    className="glass rounded-xl overflow-hidden card-hover animate-fadeIn"
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                    <div className="relative aspect-[4/3] bg-gradient-to-br from-gray-100 to-gray-200">
                      <img
                        src={img.preview}
                        alt={img.file.name}
                        className="w-full h-full object-contain"
                      />
                      <button
                        onClick={() => removeImage(index)}
                        className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition-all duration-200 shadow-lg hover:scale-110"
                        aria-label="Remove image"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                    <div className="p-4">
                      <p className="font-medium text-gray-800 truncate" title={img.file.name}>
                        {img.file.name}
                      </p>
                      <div className="flex items-center gap-2 mt-2 text-xs text-gray-600">
                        <span className="inline-flex items-center gap-1">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          {img.width} × {img.height}
                        </span>
                        <span className="inline-flex items-center gap-1">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                          </svg>
                          {(img.file.size / 1024).toFixed(1)} KB
                        </span>
                      </div>
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