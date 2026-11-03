# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 現在の段階（企画し直し中）

- 流れはスキル `app-dev-lifecycle`（0〜10）、0〜3 の詳細は `app-requirements`。段階の終わりは AskUserQuestion で承認を取る
- 現在: **3 ヒアリング 開始前（2 案出しは完了: 案は「フォルダまるごと軽量化」）**（モック: https://claude.ai/artifact/HgL5pb6fUFPvFjDGtokzNc ）（2026-11-04。1 先行研究は承認済み: `docs/01-research/summary.md`）。上位 3 案はモック（Artifact＋`docs/mock/`）で比べてから選ぶ
- 前提と決定: `docs/00-brief.md`、`docs/decisions.md`。成果物は `docs/<番号>-<名前>.md`、委譲の指示文は `logs/prompts/`
- 期限 1 か月・週 5 時間。見た目は GitHub（Primer）に寄せる。codex CLI は Web 調査と read-only レビューに使ってよい

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
    ├── imageProcessor.ts        # Image processing utilities
    └── browserCompat.ts         # Browser format support detection
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

The app is a static SPA. Production: every push to `main` deploys to GitHub Pages via `.github/workflows/deploy.yml` (https://kamata-cz.github.io/image-converter/). So pushing to main publishes immediately — confirm with the user first. `netlify.toml` is a leftover alternative.

No server-side processing or API required - all processing is client-side.
