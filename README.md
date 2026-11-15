# LayerSeparator Sample Outputs

Downloadable sample archives for inspecting bitmap image-to-layer outputs associated with [LayerSeparator](https://layerseparator.com/). Each archive pairs a flat input image with WebP layer previews, a layered PSD sample, and a nested ZIP containing PNG layers and `manifest.json`.

## Purpose and Audience

This repository lets you inspect separated layer files and their current limitations directly:

- **Designers** can evaluate mask edges, separated shadows, rasterized lettering, and reconstructed backgrounds to gauge manual cleanup effort.
- **Developers** can inspect archive layout, image dimensions, alpha transparency, and `manifest.json` structure before working with layered outputs.
- **Prospective users** can examine samples locally to see what bitmap layer separation produces and where touch-up may be needed.

## Sample Comparison

Layer counts include the `Background (filled)` layer. The output canvas is the `canvas` recorded in the nested ZIP's manifest. Individual PNG files can have different dimensions; they are not necessarily full-canvas images.

| Archive | `source.webp` size | Manifest output canvas | Layers (including background) | Download |
| --- | --- | --- | --- | --- |
| Coffee poster | 1200 × 1600 | 864 × 1152 | 5 | [coffee-sample.zip](./coffee-sample.zip) |
| Headphones | 896 × 1120 | 896 × 1120 | 5 | [headphones-sample.zip](./headphones-sample.zip) |
| Illustration | 896 × 1120 | 896 × 1120 | 8 | [illustration-sample.zip](./illustration-sample.zip) |

> **Provenance and verification:** The PSD and PNG packages for the headphones and illustration samples were assembled offline from existing public preview assets. Do not treat them as unmodified production exports. ZIP integrity and PSD file headers have been checked, but the PSD files have not yet been opened and verified in an editor. Compatibility with specific editors is not claimed.

## Preview the Inputs

| Coffee poster | Headphones | Illustration |
| --- | --- | --- |
| ![Coffee poster sample](./coffee-preview.webp) | ![Headphones sample](./headphones-preview.webp) | ![Illustration sample](./illustration-preview.webp) |

These are input previews. Download the archives above to inspect the separated layers. The machine-readable [index.json](./index.json) lists each sample's manifest canvas, layer names and archive.

## What to Observe in Each Sample

### Coffee poster

The five layers are `Background (filled)`, `English headline block`, `Decorative leaf sprig`, `Coffee cup`, and `Price badge`.

Compare the source image with the output canvas. Inspect fine contours around the leaf, edges around the headline and price badge, and the background around the cup and other elements. The output canvas differs in size from `source.webp`, so check the manifest before attempting to align the files.

### Headphones

The five layers are `Background (filled)`, `Product drop shadow`, `Headline text SOUND, UNFOLDED`, `Headphones product`, and `Price tag $129`.

Inspect the soft transparency around the product shadow, the edges of the headline and price tag, and the filled background. This PSD and PNG package was assembled offline from public preview assets.

### Illustration

The eight layers are `Background (filled)`, `Left green tree`, `Right green tree`, `Sun`, `Left cloud`, `Right cloud`, `Yellow bicycle`, and `Boy with red helmet`.

Inspect how the bicycle, person, trees, sun, and clouds are separated, especially where shapes touch or overlap. Compare them with the filled background. This PSD and PNG package was assembled offline from public preview assets.

## Archive Structure

Each outer archive contains:

```text
<name>-sample.zip
├── source.webp          # Sample input image
├── layer-N.webp         # Layer preview images
├── sample-layers.psd    # PSD sample; header checked, not editor verified
└── sample-layers.zip    # PNG layers and manifest.json
```

In the coffee sample, PNG files are at the root of the nested ZIP. In the headphones and illustration samples, PNG files are under `layers/`. Each nested ZIP includes `manifest.json`. Individual layer images may be smaller or larger than the manifest canvas, so inspect their dimensions and metadata instead of assuming a full-canvas layout.

## How to Extract and Inspect

Download an archive from the table above, then extract it and the nested PNG archive. For example, with `unzip` installed:

```bash
mkdir -p inspect-coffee
unzip ./coffee-sample.zip -d inspect-coffee
unzip inspect-coffee/sample-layers.zip -d inspect-coffee/png-layers
```

1. **Compare previews.** View `source.webp` alongside the `layer-N.webp` files to see how elements were separated.
2. **Inspect PNGs and metadata.** Open the PNG files against a checkerboard background and examine their transparency and dimensions. Read `manifest.json` for the output canvas and layer metadata. Paths and dimensions differ between samples.
3. **Inspect the PSD.** If you open `sample-layers.psd` in a design tool, check whether the file opens and whether layers, visibility, alignment, transparency, and stacking appear as expected. Editor compatibility has not yet been verified for these samples.

## Inspect an Archive with Python

The optional [inspect_sample.py](./inspect_sample.py) uses the Python 3 standard library to check ZIP integrity and file signatures, and lists the recorded canvas, layer names and PNG dimensions without extracting files:

```bash
python3 inspect_sample.py coffee-sample.zip
```

The check does not validate PSD rendering, layer alignment, or editor compatibility. It reads the nested ZIP into memory and is intended for the small sample archives in this repository.

## Evaluation Checklist

Layer separation does not guarantee exact restoration. Before reusing the samples, review:

- **Edges:** Zoom in on thin details and rasterized text for rough masks, clipped strokes, or color fringes.
- **Background:** Inspect `Background (filled)` for seams or texture artifacts in areas covered by foreground elements in the source.
- **Occlusion:** Check where objects touch or overlap; moving a layer may expose areas that need retouching.
- **Dimensions and alignment:** The manifest output canvas is not necessarily the same size as the source or individual layer files. Check the image dimensions and metadata before compositing.
- **Stacking:** Review layer order when inspecting the PSD or assembling PNGs so that shadows, subjects, and decorations appear as intended.

## FAQ

### Is text directly editable?

No. The sample layers are raster bitmaps. The text visible in the layers consists of pixels rather than editable font objects.

### How is the background produced?

Areas hidden by foreground elements in the source are represented by reconstructed content. These are filled pixels, not original hidden pixels recovered from the flat source image.

### Why can dimensions differ?

The coffee sample's source is 1200 × 1600, while its manifest records an 864 × 1152 output canvas. The other two source images and their recorded output canvases are 896 × 1120. Individual PNG layers can have different dimensions. Internal resizing rules are not specified here; inspect the files and manifest before compositing.

### Will I need manual adjustments?

Depending on the edit, edges, occluded areas, stacking order, and background fills may need review and touch-up. Inspect the samples for your intended use.

## Download and Reuse

The sample owner permits public download and reuse of these archives. Specific license terms have not yet been determined; no formal license identifier, attribution requirement, or commercial-use condition has been established. Exact licensing terms remain pending.

## Product Links

- [LayerSeparator](https://layerseparator.com/)
- [Image to PSD](https://layerseparator.com/image-to-psd)
