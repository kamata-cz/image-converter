import { useState, useEffect } from 'react';
import {
  processImage,
  downloadImage,
  generateFilename,
  type ConversionOptions,
  type ResizeOptions,
} from '../utils/imageProcessor';

interface ImageFile {
  file: File;
  preview: string;
  width: number;
  height: number;
}

interface ImageConverterProps {
  images: ImageFile[];
  onProcessComplete?: () => void;
}

interface Settings {
  format: 'png' | 'jpeg' | 'webp' | 'avif';
  quality: number;
  resizeWidth: number;
  resizeHeight: number;
  maintainAspectRatio: boolean;
  resizeMode: 'cover' | 'contain' | 'stretch';
}

export function ImageConverter({ images, onProcessComplete }: ImageConverterProps) {
  const [settings, setSettings] = useState<Settings>({
    format: 'png',
    quality: 90,
    resizeWidth: 0,
    resizeHeight: 0,
    maintainAspectRatio: true,
    resizeMode: 'contain',
  });

  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);

  // Load settings from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('imageConverterSettings');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setSettings(parsed);
      } catch (e) {
        console.error('Failed to load settings', e);
      }
    }
  }, []);

  // Save settings to localStorage
  useEffect(() => {
    localStorage.setItem('imageConverterSettings', JSON.stringify(settings));
  }, [settings]);

  const handleConvert = async () => {
    if (images.length === 0) return;

    setProcessing(true);
    setProgress(0);

    const resizeOptions: ResizeOptions = {
      width: settings.resizeWidth || undefined,
      height: settings.resizeHeight || undefined,
      maintainAspectRatio: settings.maintainAspectRatio,
      mode: settings.resizeMode,
    };

    const conversionOptions: ConversionOptions = {
      format: settings.format,
      quality: settings.quality / 100,
    };

    try {
      for (let i = 0; i < images.length; i++) {
        const image = images[i];
        const processed = await processImage(image.file, resizeOptions, conversionOptions);

        const filename = generateFilename(
          image.file.name,
          processed.width,
          processed.height,
          processed.format
        );

        downloadImage(processed.blob, filename);

        setProgress(((i + 1) / images.length) * 100);
      }

      onProcessComplete?.();
    } catch (error) {
      console.error('Processing failed:', error);
      alert('Failed to process images. Please try again.');
    } finally {
      setProcessing(false);
      setProgress(0);
    }
  };

  if (images.length === 0) {
    return null;
  }

  return (
    <div className="mt-8 bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">Conversion Settings</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Output Format */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Output Format
          </label>
          <select
            value={settings.format}
            onChange={(e) =>
              setSettings({ ...settings, format: e.target.value as Settings['format'] })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="png">PNG</option>
            <option value="jpeg">JPEG</option>
            <option value="webp">WebP</option>
            <option value="avif">AVIF</option>
          </select>
        </div>

        {/* Quality */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Quality: {settings.quality}%
          </label>
          <input
            type="range"
            min="1"
            max="100"
            value={settings.quality}
            onChange={(e) => setSettings({ ...settings, quality: Number(e.target.value) })}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        {/* Resize Width */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Width (px, 0 = original)
          </label>
          <input
            type="number"
            min="0"
            value={settings.resizeWidth}
            onChange={(e) =>
              setSettings({ ...settings, resizeWidth: Number(e.target.value) })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Resize Height */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Height (px, 0 = original)
          </label>
          <input
            type="number"
            min="0"
            value={settings.resizeHeight}
            onChange={(e) =>
              setSettings({ ...settings, resizeHeight: Number(e.target.value) })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Maintain Aspect Ratio */}
        <div className="flex items-center">
          <input
            type="checkbox"
            id="maintainAspectRatio"
            checked={settings.maintainAspectRatio}
            onChange={(e) =>
              setSettings({ ...settings, maintainAspectRatio: e.target.checked })
            }
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <label htmlFor="maintainAspectRatio" className="ml-2 text-sm text-gray-700">
            Maintain aspect ratio
          </label>
        </div>

        {/* Resize Mode */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Resize Mode</label>
          <select
            value={settings.resizeMode}
            onChange={(e) =>
              setSettings({
                ...settings,
                resizeMode: e.target.value as Settings['resizeMode'],
              })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="contain">Contain (fit inside)</option>
            <option value="cover">Cover (fill area)</option>
            <option value="stretch">Stretch (ignore ratio)</option>
          </select>
        </div>
      </div>

      {/* Convert Button */}
      <div className="mt-6">
        <button
          onClick={handleConvert}
          disabled={processing}
          className="w-full bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
        >
          {processing
            ? `Processing... ${Math.round(progress)}%`
            : `Convert ${images.length} Image${images.length > 1 ? 's' : ''}`}
        </button>
      </div>

      {/* Progress Bar */}
      {processing && (
        <div className="mt-4">
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-green-600 h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      )}
    </div>
  );
}
