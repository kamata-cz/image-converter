# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Browser-based image conversion tool built with React, TypeScript, and TailwindCSS. The application performs all image processing client-side using Canvas API and createImageBitmap.

## Commands

### Development
```bash
npm run dev          # Start development server (http://localhost:5173)
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
```

## Architecture

### Core Components

- **App.tsx**: Main application component handling file upload and drag-and-drop
- **ImageConverter.tsx**: Conversion settings panel with quality, format, and resize controls
- **imageProcessor.ts**: Core image processing utilities

### Key Features

1. **Image Processing Pipeline**
   - EXIF orientation detection and correction
   - Resize with aspect ratio modes (cover/contain/stretch)
   - Format conversion (PNG/JPEG/WebP/AVIF)
   - Quality/compression controls

2. **User Interface**
   - Drag-and-drop file upload
   - Multi-file batch processing
   - Real-time preview
   - Progress indicators

3. **Settings Persistence**
   - Settings saved to LocalStorage
   - Automatic restore on page load

### Image Processing Flow

1. File upload → createImageBitmap()
2. EXIF orientation reading (imageProcessor.ts:22)
3. Canvas transformation based on orientation
4. Resize calculation (imageProcessor.ts:85)
5. Canvas draw with high quality smoothing
6. toBlob() conversion with quality settings
7. Download with filename template

### Important Implementation Details

- **EXIF Handling**: Orientation values 5-8 require width/height swap (imageProcessor.ts:138)
- **Canvas Quality**: Always use `imageSmoothingQuality = 'high'` for best results
- **Format Support**: Browser native support checked for WebP/AVIF, fallback to Canvas
- **Filename Template**: `{basename}_{width}x{height}.{ext}` format (imageProcessor.ts:188)

## File Structure

```
src/
├── App.tsx                      # Main app component
├── components/
│   └── ImageConverter.tsx       # Settings and conversion UI
└── utils/
    └── imageProcessor.ts        # Image processing utilities
```

## Dependencies

- **React 19**: UI framework
- **Vite**: Build tool and dev server
- **TailwindCSS 4**: Styling (uses @tailwindcss/postcss plugin)
- **TypeScript**: Type checking

## Adding New Features

### Adding New Image Format

1. Update `ConversionOptions` type in imageProcessor.ts
2. Add MIME type handling in `processImage()` function
3. Update format selector in ImageConverter.tsx
4. Test browser support and add fallback if needed

### Adding New Resize Mode

1. Add mode to `ResizeOptions` type
2. Implement calculation in `calculateDimensions()` function
3. Add option to resize mode selector in ImageConverter.tsx

## Testing

Manual testing checklist:
- Upload various image formats (JPEG, PNG, WebP, AVIF)
- Test EXIF rotated images (particularly orientation 6 and 8)
- Verify resize with different modes
- Test batch processing
- Check LocalStorage persistence
- Verify downloads with correct filenames

## Deployment

The app is a static SPA. Build with `npm run build` and deploy the `dist/` folder to any static hosting:
- Vercel: `vercel deploy`
- Netlify: `netlify deploy --prod --dir=dist`
- GitHub Pages: Deploy dist folder to gh-pages branch

No server-side processing or API required - all processing is client-side.
