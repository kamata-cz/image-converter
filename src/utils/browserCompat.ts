/**
 * Browser Compatibility Utilities
 * Provides feature detection and polyfills for cross-browser support
 */

export interface BrowserFeatures {
  canvas: boolean;
  fileAPI: boolean;
  dragAndDrop: boolean;
  backdropFilter: boolean;
  webp: boolean;
  avif: boolean;
  createImageBitmap: boolean;
  offscreenCanvas: boolean;
  webWorkers: boolean;
}

/**
 * Detect browser features and capabilities
 */
export function detectBrowserFeatures(): BrowserFeatures {
  const features: BrowserFeatures = {
    canvas: false,
    fileAPI: false,
    dragAndDrop: false,
    backdropFilter: false,
    webp: false,
    avif: false,
    createImageBitmap: false,
    offscreenCanvas: false,
    webWorkers: false,
  };

  // Canvas support
  try {
    const canvas = document.createElement('canvas');
    features.canvas = !!(canvas.getContext && canvas.getContext('2d'));
  } catch (e) {
    features.canvas = false;
  }

  // File API support
  features.fileAPI = !!(
    window.File &&
    window.FileReader &&
    window.FileList &&
    window.Blob
  );

  // Drag and Drop support
  const div = document.createElement('div');
  features.dragAndDrop = 'draggable' in div || ('ondragstart' in div && 'ondrop' in div);

  // Backdrop filter support
  if (CSS && CSS.supports) {
    features.backdropFilter =
      CSS.supports('backdrop-filter', 'blur(10px)') ||
      CSS.supports('-webkit-backdrop-filter', 'blur(10px)');
  }

  // WebP support detection
  features.webp = checkImageFormatSupport('webp');

  // AVIF support detection
  features.avif = checkImageFormatSupport('avif');

  // createImageBitmap support
  features.createImageBitmap = typeof createImageBitmap === 'function';

  // OffscreenCanvas support
  features.offscreenCanvas = typeof OffscreenCanvas !== 'undefined';

  // Web Workers support
  features.webWorkers = typeof Worker !== 'undefined';

  return features;
}

/**
 * Check if specific image format is supported
 */
function checkImageFormatSupport(format: string): boolean {
  const canvas = document.createElement('canvas');
  canvas.width = 1;
  canvas.height = 1;
  const ctx = canvas.getContext('2d');

  if (!ctx) return false;

  try {
    const dataURL = canvas.toDataURL(`image/${format}`);
    return dataURL.indexOf(`image/${format}`) === 5;
  } catch (e) {
    return false;
  }
}

/**
 * Get browser information
 */
export function getBrowserInfo() {
  const ua = navigator.userAgent;
  const platform = navigator.platform;

  return {
    isChrome: /Chrome/.test(ua) && /Google Inc/.test(navigator.vendor),
    isSafari: /Safari/.test(ua) && /Apple Computer/.test(navigator.vendor),
    isFirefox: /Firefox/.test(ua),
    isEdge: /Edg/.test(ua),
    isArc: /Arc/.test(ua), // Arc browser detection
    isMobile: /Mobi|Android|iPhone|iPad|iPod/.test(ua),
    platform,
    userAgent: ua,
  };
}

/**
 * Check if all required features are supported
 */
export function checkRequiredFeatures(): { supported: boolean; missing: string[] } {
  const features = detectBrowserFeatures();
  const missing: string[] = [];

  // Required features for the app to work
  if (!features.canvas) missing.push('Canvas API');
  if (!features.fileAPI) missing.push('File API');

  return {
    supported: missing.length === 0,
    missing,
  };
}

/**
 * Get optimal image format based on browser support
 */
export function getOptimalImageFormat(preferredFormat?: string): string {
  const features = detectBrowserFeatures();

  if (preferredFormat) {
    switch (preferredFormat) {
      case 'avif':
        if (features.avif) return 'avif';
        break;
      case 'webp':
        if (features.webp) return 'webp';
        break;
      default:
        return preferredFormat;
    }
  }

  // Fallback chain
  if (features.avif) return 'avif';
  if (features.webp) return 'webp';
  return 'jpeg';
}

/**
 * Apply browser-specific fixes
 */
export function applyBrowserFixes(): void {
  const browserInfo = getBrowserInfo();
  const html = document.documentElement;

  // Add browser-specific classes
  if (browserInfo.isArc) {
    html.classList.add('browser-arc');
  }
  if (browserInfo.isSafari) {
    html.classList.add('browser-safari');
  }
  if (browserInfo.isFirefox) {
    html.classList.add('browser-firefox');
  }
  if (browserInfo.isChrome) {
    html.classList.add('browser-chrome');
  }
  if (browserInfo.isEdge) {
    html.classList.add('browser-edge');
  }

  // Apply mobile-specific fixes
  if (browserInfo.isMobile) {
    html.classList.add('is-mobile');

    // Disable hover effects on mobile
    const style = document.createElement('style');
    style.textContent = `
      @media (hover: none) {
        .card-hover:hover {
          transform: none !important;
        }
        .btn-gradient:hover {
          transform: none !important;
        }
      }
    `;
    document.head.appendChild(style);
  }

  // Safari-specific fixes
  if (browserInfo.isSafari) {
    // Fix for Safari's backdrop-filter
    const style = document.createElement('style');
    style.textContent = `
      .browser-safari .glass {
        -webkit-backdrop-filter: saturate(180%) blur(10px);
        backdrop-filter: saturate(180%) blur(10px);
      }
    `;
    document.head.appendChild(style);
  }

  // Arc browser specific optimizations
  if (browserInfo.isArc) {
    const style = document.createElement('style');
    style.textContent = `
      .browser-arc .glass {
        background: rgba(255, 255, 255, 0.92);
      }
      .browser-arc .btn-gradient {
        will-change: transform;
      }
    `;
    document.head.appendChild(style);
  }
}

/**
 * Show compatibility warning if needed
 */
export function showCompatibilityWarning(): void {
  const { supported, missing } = checkRequiredFeatures();

  if (!supported) {
    console.warn('Browser compatibility issues detected:', missing);

    // Create warning element
    const warning = document.createElement('div');
    warning.className = 'browser-warning';
    warning.innerHTML = `
      <strong>Browser Compatibility Warning:</strong>
      Your browser is missing the following features: ${missing.join(', ')}.
      Some functionality may not work correctly.
    `;
    warning.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      background: #ff9800;
      color: white;
      padding: 12px;
      text-align: center;
      z-index: 10000;
      font-family: system-ui, -apple-system, sans-serif;
    `;

    document.body.insertBefore(warning, document.body.firstChild);

    // Auto-hide after 10 seconds
    setTimeout(() => {
      warning.style.display = 'none';
    }, 10000);
  }
}

/**
 * Initialize browser compatibility fixes
 */
export function initBrowserCompat(): void {
  // Apply fixes as soon as DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      applyBrowserFixes();
      showCompatibilityWarning();
    });
  } else {
    applyBrowserFixes();
    showCompatibilityWarning();
  }

  // Log browser info for debugging
  if (import.meta.env.DEV) {
    console.log('Browser Info:', getBrowserInfo());
    console.log('Browser Features:', detectBrowserFeatures());
  }
}