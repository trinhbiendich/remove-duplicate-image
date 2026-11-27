# Remove Duplicate Image

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-2.7-3776AB?logo=python&logoColor=white)](https://www.python.org/)

A lightweight Python CLI tool that recursively scans an image directory, detects duplicate and visually similar images using 64-bit perceptual average hashing (aHash) and Hamming distance, and moves smaller-width duplicates and non-image files into an output folder.

## Key Features

- **Recursive Directory Scanning**: Walks the entire input folder and all subdirectories for `.jpg`, `.jpeg`, and `.png` images.
- **Perceptual Similarity Detection (aHash)**: Resizes each image to 8×8 grayscale, computes a 64-bit average hash, and compares image pairs via Hamming distance to calculate a similarity percentage.
- **Configurable Similarity Threshold**: Customize the minimum similarity percentage (`-max` / `--percentsame`, default `95%`) to match exact or near-duplicate images.
- **Keeps Higher-Resolution Images**: When two images match at or above the threshold, the image with the smaller width is moved to the output directory while the wider image stays in place.
- **Non-Image Filtering**: Validates image headers with `imghdr` and moves unsupported or invalid files into `<output>/not_img/`.
- **Safe Filename Collision Handling**: Automatically assigns a UUID-based filename if a file with the same name already exists in the destination folder.

## Tech Stack

- **Language**: Python (Python 2 syntax — uses `print` statements, `reduce`, and `imghdr`)
- **Image Processing**: [Pillow / PIL](https://pillow.readthedocs.io/) (`PIL.Image`)
- **Standard Library**: `argparse`, `os`, `imghdr`, `shutil`, `uuid`, `sys`

## Project Structure

```text
remove-duplicate-image/
├── removedup.py   # CLI script for perceptual hashing, duplicate detection, and file moving
├── README.md      # Project documentation
└── LICENSE        # MIT License
```

## Prerequisites

- **Python 2.7** (the script uses Python 2 syntax and `Image.ANTIALIAS`)
- **Pillow** (or PIL) compatible with Python 2.7:

```bash
pip install Pillow
```

## Usage

Run the script by specifying an input folder (`-i`) and an output folder (`-o`), with an optional similarity threshold (`-max`):

```bash
python removedup.py -i pics -o imgs -max 95
```

### CLI Options

| Flag | Long Flag | Required | Default | Description |
| :--- | :--- | :---: | :---: | :--- |
| `-i` | `--input` | Yes | — | Path to the input directory containing images to scan |
| `-o` | `--output` | Yes | — | Output directory where detected duplicate images are moved |
| `-max` | `--percentsame` | No | `95` | Minimum similarity percentage (`0`–`100`) to treat two images as duplicates |

### Behavior Notes

- The output directory and `<output>/not_img/` are created automatically if they do not exist.
- Duplicate images and non-image files are **moved** (not copied) out of the input directory, so back up your files first if needed.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
