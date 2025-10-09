# Image Converter

A browser-based image conversion tool that allows you to convert, resize, and compress images entirely in the browser. Built with React, TypeScript, and TailwindCSS.

## Features

- **Format Conversion**: Convert between PNG, JPEG, WebP, and AVIF
- **Image Resize**: Resize images with aspect ratio control
- **Quality Control**: Adjust compression quality
- **EXIF Orientation**: Automatic handling of image orientation
- **Batch Processing**: Process multiple images at once
- **Local Processing**: All processing happens in the browser - no uploads required
- **Settings Persistence**: Your settings are saved locally

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

### Linting & Formatting

```bash
npm run lint
npm run format
```

## Usage

1. **Upload Images**: Drag and drop images or click to select files
2. **Configure Settings**:
   - Choose output format (PNG, JPEG, WebP, AVIF)
   - Adjust quality slider
   - Set resize dimensions (optional)
   - Select resize mode
3. **Convert**: Click the convert button to process and download images

## Technology Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS 4** - Styling
- **Canvas API** - Image processing
- **createImageBitmap** - High-performance image decoding

## Browser Support

- Chrome 110+
- Firefox 116+
- Safari 16.4+
- Edge 110+

## Privacy

All image processing is done locally in your browser. No images are uploaded to any server.

## License

MIT
