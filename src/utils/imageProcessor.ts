export interface ResizeOptions {
  width?: number;
  height?: number;
  maintainAspectRatio?: boolean;
  mode?: 'cover' | 'contain' | 'stretch';
}

export interface ConversionOptions {
  format: 'png' | 'jpeg' | 'webp' | 'avif';
  quality?: number;
}

export interface ProcessedImage {
  blob: Blob;
  width: number;
  height: number;
  format: string;
}

// Read EXIF orientation and get proper rotation/flip values
export function getExifOrientation(file: File): Promise<number> {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const view = new DataView(e.target?.result as ArrayBuffer);
      if (view.getUint16(0, false) !== 0xffd8) {
        resolve(1); // Not a JPEG
        return;
      }
      const length = view.byteLength;
      let offset = 2;
      while (offset < length) {
        if (view.getUint16(offset + 2, false) <= 8) {
          resolve(1);
          return;
        }
        const marker = view.getUint16(offset, false);
        offset += 2;
        if (marker === 0xffe1) {
          const little = view.getUint16((offset += 6), false) === 0x4949;
          offset += view.getUint32(offset + 4, little);
          const tags = view.getUint16(offset, little);
          offset += 2;
          for (let i = 0; i < tags; i++) {
            if (view.getUint16(offset + i * 12, little) === 0x0112) {
              resolve(view.getUint16(offset + i * 12 + 8, little));
              return;
            }
          }
        } else if ((marker & 0xff00) !== 0xff00) {
          break;
        } else {
          offset += view.getUint16(offset, false);
        }
      }
      resolve(1);
    };
    reader.onerror = () => resolve(1);
    reader.readAsArrayBuffer(file);
  });
}

// Apply EXIF orientation to canvas
export function applyOrientation(
  ctx: CanvasRenderingContext2D,
  orientation: number,
  width: number,
  height: number
): void {
  switch (orientation) {
    case 2:
      ctx.transform(-1, 0, 0, 1, width, 0);
      break;
    case 3:
      ctx.transform(-1, 0, 0, -1, width, height);
      break;
    case 4:
      ctx.transform(1, 0, 0, -1, 0, height);
      break;
    case 5:
      ctx.transform(0, 1, 1, 0, 0, 0);
      break;
    case 6:
      ctx.transform(0, 1, -1, 0, height, 0);
      break;
    case 7:
      ctx.transform(0, -1, -1, 0, height, width);
      break;
    case 8:
      ctx.transform(0, -1, 1, 0, 0, width);
      break;
  }
}

// Calculate new dimensions based on resize options
export function calculateDimensions(
  originalWidth: number,
  originalHeight: number,
  options: ResizeOptions
): { width: number; height: number } {
  const { width, height, maintainAspectRatio = true, mode = 'contain' } = options;

  if (!width && !height) {
    return { width: originalWidth, height: originalHeight };
  }

  if (maintainAspectRatio) {
    const aspectRatio = originalWidth / originalHeight;

    if (width && height) {
      if (mode === 'cover') {
        const scale = Math.max(width / originalWidth, height / originalHeight);
        return {
          width: Math.round(originalWidth * scale),
          height: Math.round(originalHeight * scale),
        };
      } else if (mode === 'contain') {
        const scale = Math.min(width / originalWidth, height / originalHeight);
        return {
          width: Math.round(originalWidth * scale),
          height: Math.round(originalHeight * scale),
        };
      }
    }

    if (width) {
      return { width, height: Math.round(width / aspectRatio) };
    }

    if (height) {
      return { width: Math.round(height * aspectRatio), height };
    }
  }

  return {
    width: width || originalWidth,
    height: height || originalHeight,
  };
}

// Resize and convert image
export async function processImage(
  file: File,
  resizeOptions: ResizeOptions = {},
  conversionOptions: ConversionOptions = { format: 'png', quality: 0.9 }
): Promise<ProcessedImage> {
  const orientation = await getExifOrientation(file);
  const img = await createImageBitmap(file);

  const { width: newWidth, height: newHeight } = calculateDimensions(
    img.width,
    img.height,
    resizeOptions
  );

  // Handle orientation swap for rotated images
  const needsSwap = orientation >= 5 && orientation <= 8;
  const canvas = document.createElement('canvas');
  canvas.width = needsSwap ? newHeight : newWidth;
  canvas.height = needsSwap ? newWidth : newHeight;

  const ctx = canvas.getContext('2d');
  if (!ctx) {
    throw new Error('Failed to get canvas context');
  }

  // Apply orientation transformation
  if (orientation !== 1) {
    applyOrientation(ctx, orientation, canvas.width, canvas.height);
  }

  // Draw with high quality
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';
  ctx.drawImage(img, 0, 0, newWidth, newHeight);

  // Convert to blob
  const mimeType = `image/${conversionOptions.format}`;
  const blob = await new Promise<Blob>((resolve, reject) => {
    canvas.toBlob(
      (b) => {
        if (b) resolve(b);
        else reject(new Error('Failed to convert canvas to blob'));
      },
      mimeType,
      conversionOptions.quality
    );
  });

  return {
    blob,
    width: newWidth,
    height: newHeight,
    format: conversionOptions.format,
  };
}

// Download processed image
export function downloadImage(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

// Generate filename with template
export function generateFilename(
  originalName: string,
  width: number,
  height: number,
  format: string
): string {
  const basename = originalName.replace(/\.[^/.]+$/, '');
  const sanitized = basename.replace(/[^a-z0-9_-]/gi, '_');
  return `${sanitized}_${width}x${height}.${format}`;
}
