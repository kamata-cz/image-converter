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

interface Preset {
  name: string;
  icon: string;
  settings: Partial<Settings>;
}

const PRESETS: Preset[] = [
  {
    name: 'Original',
    icon: '📁',
    settings: { resizeWidth: 0, resizeHeight: 0, quality: 90 },
  },
  {
    name: 'Web Optimized',
    icon: '🌐',
    settings: { format: 'webp', quality: 80, resizeWidth: 1920, maintainAspectRatio: true },
  },
  {
    name: 'Thumbnail',
    icon: '🖼️',
    settings: { resizeWidth: 400, resizeHeight: 400, resizeMode: 'cover', quality: 85 },
  },
  {
    name: 'Social Media',
    icon: '📱',
    settings: { resizeWidth: 1200, resizeHeight: 630, resizeMode: 'cover', quality: 85 },
  },
  {
    name: 'High Quality',
    icon: '✨',
    settings: { format: 'png', quality: 100, resizeWidth: 0, resizeHeight: 0 },
  },
  {
    name: 'Small File',
    icon: '🗜️',
    settings: { format: 'webp', quality: 60, resizeWidth: 1280, maintainAspectRatio: true },
  },
];

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
  const [showSuccess, setShowSuccess] = useState(false);
  const [selectedPreset, setSelectedPreset] = useState<string>('Original');

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

  const handlePresetSelect = (preset: Preset) => {
    setSettings((prev) => ({ ...prev, ...preset.settings }));
    setSelectedPreset(preset.name);
  };

  const handleConvert = async () => {
    if (images.length === 0) return;

    setProcessing(true);
    setProgress(0);
    setShowSuccess(false);

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

      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
      onProcessComplete?.();
    } catch (error) {
      console.error('Processing failed:', error);
      alert('Failed to process images. Please try again.');
    } finally {
      setProcessing(false);
      setTimeout(() => setProgress(0), 500);
    }
  };

  const resetSettings = () => {
    const defaultSettings: Settings = {
      format: 'png',
      quality: 90,
      resizeWidth: 0,
      resizeHeight: 0,
      maintainAspectRatio: true,
      resizeMode: 'contain',
    };
    setSettings(defaultSettings);
    setSelectedPreset('Original');
  };

  if (images.length === 0) {
    return null;
  }

  return (
    <div className="mt-10 space-y-6">
      {/* Presets */}
      <div className="glass rounded-2xl p-6 animate-fadeIn">
        <h3 className="text-lg font-bold text-gray-800 mb-4">Quick Presets</h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
          {PRESETS.map((preset) => (
            <button
              key={preset.name}
              onClick={() => handlePresetSelect(preset)}
              className={`
                p-3 rounded-xl text-center transition-all duration-200
                ${selectedPreset === preset.name
                  ? 'bg-gradient-to-r from-purple-500 to-purple-600 text-white shadow-lg scale-105'
                  : 'bg-white/60 hover:bg-white/80 text-gray-700 hover:shadow-md'
                }
              `}
            >
              <div className="text-2xl mb-1">{preset.icon}</div>
              <div className="text-xs font-medium">{preset.name}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Settings */}
      <div className="glass rounded-2xl p-6 animate-fadeIn">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Conversion Settings</h2>
          <button
            onClick={resetSettings}
            className="text-sm text-purple-600 hover:text-purple-700 font-medium transition-colors"
          >
            Reset Settings
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Output Format */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Output Format
            </label>
            <div className="grid grid-cols-2 gap-2">
              {['png', 'jpeg', 'webp', 'avif'].map((format) => (
                <button
                  key={format}
                  onClick={() => setSettings({ ...settings, format: format as Settings['format'] })}
                  className={`
                    py-2 px-3 rounded-lg font-medium transition-all duration-200
                    ${settings.format === format
                      ? 'bg-gradient-to-r from-purple-500 to-purple-600 text-white shadow-md'
                      : 'bg-white/60 hover:bg-white/80 text-gray-700'
                    }
                  `}
                >
                  {format.toUpperCase()}
                </button>
              ))}
            </div>
          </div>

          {/* Quality */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Quality: <span className="text-purple-600 font-bold">{settings.quality}%</span>
            </label>
            <div className="relative">
              <input
                type="range"
                min="1"
                max="100"
                value={settings.quality}
                onChange={(e) => setSettings({ ...settings, quality: Number(e.target.value) })}
                className="w-full"
              />
              <div
                className="absolute top-0 left-0 h-1.5 bg-gradient-to-r from-purple-500 to-purple-600 rounded-l-full pointer-events-none"
                style={{ width: `${settings.quality}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Low</span>
              <span>High</span>
            </div>
          </div>

          {/* Resize Dimensions */}
          <div className="md:col-span-2">
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Resize Dimensions (0 = original)
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs text-gray-600 mb-1">Width (px)</label>
                <input
                  type="number"
                  min="0"
                  value={settings.resizeWidth}
                  onChange={(e) =>
                    setSettings({ ...settings, resizeWidth: Number(e.target.value) })
                  }
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                  placeholder="Auto"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-600 mb-1">Height (px)</label>
                <input
                  type="number"
                  min="0"
                  value={settings.resizeHeight}
                  onChange={(e) =>
                    setSettings({ ...settings, resizeHeight: Number(e.target.value) })
                  }
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                  placeholder="Auto"
                />
              </div>
              <div className="flex items-end">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.maintainAspectRatio}
                    onChange={(e) =>
                      setSettings({ ...settings, maintainAspectRatio: e.target.checked })
                    }
                    className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500 mr-2"
                  />
                  <span className="text-sm text-gray-700">Keep aspect ratio</span>
                </label>
              </div>
            </div>
          </div>

          {/* Resize Mode */}
          <div className="md:col-span-2">
            <label className="block text-sm font-semibold text-gray-700 mb-3">Resize Mode</label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { value: 'contain', label: 'Contain', desc: 'Fit inside dimensions' },
                { value: 'cover', label: 'Cover', desc: 'Fill entire area' },
                { value: 'stretch', label: 'Stretch', desc: 'Ignore aspect ratio' },
              ].map((mode) => (
                <button
                  key={mode.value}
                  onClick={() =>
                    setSettings({
                      ...settings,
                      resizeMode: mode.value as Settings['resizeMode'],
                    })
                  }
                  className={`
                    p-3 rounded-lg text-center transition-all duration-200
                    ${settings.resizeMode === mode.value
                      ? 'bg-gradient-to-r from-purple-500 to-purple-600 text-white shadow-md'
                      : 'bg-white/60 hover:bg-white/80 text-gray-700'
                    }
                  `}
                >
                  <div className="font-medium">{mode.label}</div>
                  <div className="text-xs mt-1 opacity-80">{mode.desc}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Convert Button */}
        <div className="mt-8">
          <button
            onClick={handleConvert}
            disabled={processing}
            className={`
              w-full py-4 rounded-xl font-semibold text-lg transition-all duration-300 transform
              ${processing
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white shadow-lg hover:shadow-xl hover:-translate-y-1'
              }
            `}
          >
            {processing ? (
              <span className="flex items-center justify-center gap-3">
                <span className="spinner w-5 h-5 border-2"></span>
                Processing... {Math.round(progress)}%
              </span>
            ) : (
              `Convert ${images.length} Image${images.length > 1 ? 's' : ''}`
            )}
          </button>
        </div>

        {/* Progress Bar */}
        {processing && (
          <div className="mt-4">
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div
                className="progress-gradient h-full rounded-full transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Success Toast */}
      {showSuccess && (
        <div className="toast bg-gradient-to-r from-green-500 to-emerald-600 text-white">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          <span className="font-medium">Images converted successfully!</span>
        </div>
      )}
    </div>
  );
}