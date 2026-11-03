# Image Converter

日本語: [README.md](README.md)

A web tool that converts images entirely inside your browser. Images are never uploaded to a server.

- Live site: https://kamata-cz.github.io/image-converter/
- Note: the project is being re-planned. See "What's next".

## Features

The UI is English only (not localized).

### Confirmed working

Checked on 2026-11-04 by operating the live site in headless Chrome.

- Selecting an image with the file button (one image)
- PNG to WebP conversion and download
- The quality slider shows and changes its value (quality has no effect on PNG; this is a browser limitation)

### In the code, but not verified

These are implemented but have not been exercised.

- Adding images by drag and drop
- JPEG and PNG output
- Resize (width/height, keep aspect ratio, contain / cover / stretch). Note: cover currently outputs the enlarged size without cropping.
- Six presets (Original / Web Optimized / Thumbnail / Social Media / High Quality / Small File)
- EXIF orientation correction (EXIF is metadata embedded in photos; JPEG only)
- Batch conversion of multiple files (each file downloads separately; no ZIP)
- Saving and restoring settings (browser LocalStorage)

Output file names follow `{basename}_{width}x{height}.{ext}`. Non-ASCII characters in names are replaced with `_`.

## Output formats by browser

Whether the browser canvas can encode each format.

| Format | Chrome / Edge | Firefox | Safari (Mac / iOS) |
|---|---|---|---|
| PNG | Yes | Yes | Yes |
| JPEG | Yes | Yes | Yes |
| WebP | Yes | Yes (96+) | No |
| AVIF | No | No | No evidence of support found; unverified |

- Sources: MDN browser-compat-data, caniuse, and a measurement on Chrome 156 (see `docs/01-research/raw/C-tech-claude.md`, section 1-1). Only Chrome was measured. Edge, Firefox, and Safari were not tested on real browsers.
- Note: AVIF encoding from canvas is not confirmed in any browser. On Chrome 156 the output was PNG.
- Note: when you pick a format the browser cannot encode, the tool switches to another format (see "Known issues").
  - On Chrome, choosing AVIF produces WebP (confirmed).
  - On Safari, choosing WebP or AVIF should produce JPEG. This is inferred from the code branches and not verified on Safari.

## Known issues

From the research notes (`docs/01-research/raw/F-existing-claude.md`, `docs/01-research/raw/C-tech-claude.md`).

- Choosing AVIF silently produces another format (WebP on Chrome). The UI shows no warning.
- EXIF orientation may be applied twice: the browser already rotates the image, then the code rotates it again. Reproduced on Chrome 156 with orientation 6. Portrait iPhone photos may come out sideways. Safari and Firefox are untested.
- Transparent images converted to JPEG get a black background (measured on Chrome 156).
- HEIC (the iPhone photo format) is not supported. If one image cannot be read, the selected images may not appear in the list (inferred from the code; not executed).
- When conversion fails, only an `alert` without a reason is shown.
- Large images are processed on the main thread, so the page can freeze. iOS is documented to limit canvas to 4,096x4,096 px, which may break large photos (unverified).
- English-only UI; accessibility (labels, aria attributes) is lacking.
- `npm run lint` fails with 2 errors (unused variable `e` at `src/utils/browserCompat.ts` lines 38 and 93).
- There are no tests.
- Leftover unused files remain, such as `.env.example` and `netlify.toml`.

## Getting started

Use Node.js 20 as the baseline (the deploy workflow `.github/workflows/deploy.yml` uses 20).

```bash
npm ci            # install dependencies
npm run dev       # dev server (http://localhost:5173)
npm run build     # production build into dist/
npm run lint      # ESLint (currently fails with 2 errors)
npm run preview   # preview the production build
npm run format    # format with Prettier
```

Main files:

- `src/App.tsx`: file selection and drag and drop
- `src/components/ImageConverter.tsx`: conversion settings UI
- `src/utils/imageProcessor.ts`: conversion, resize, and EXIF handling

Stack: React 19, TypeScript, Vite, TailwindCSS 4.

## Deployment

Pushing to `main` triggers GitHub Actions, which builds the app and publishes it to GitHub Pages.

- Lint and tests are not run before publishing. The site is published even if lint fails.
- `base` in `vite.config.ts` is `/image-converter/`. Change it if you move the site to the root of another domain.
- Note: this is a public repository; anything you push is readable by anyone.

## What's next

The project is being re-planned on top of this existing tool. Progress and research are recorded in `docs/`.

- [docs/decisions.md](docs/decisions.md): decision log
- [docs/01-research/summary.md](docs/01-research/summary.md): research summary
- [docs/00-brief.md](docs/00-brief.md): project brief

Direction may change, and so may the feature list above.

## License

Not decided yet. There is no LICENSE file. It will be decided together with the monetization plan.
