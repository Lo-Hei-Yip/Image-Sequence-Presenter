# Image-Sequence-Presenter

This repository contains a Python program designed for presenting a randomized sequence of PNG images (e.g., symbols like arrows) on a full-screen display. It is used in the Final Year Project (FYP) titled _Mind-to-Screen: EEG-Driven Symbol Generation for Assistive Communication_ by Lo Hei Yip (SID: 1155195182). The program's primary purpose is to generate a controlled visual stimulus sequence for acquiring EEG data during model training. It displays each image, followed by an "imagine" phase (black screen) where participants mentally visualize the symbol, and a rest phase. Timestamps for the imagine phase are logged to a CSV file for synchronization with EEG recordings from tools like the OpenBCI GUI.

The program uses Pygame for rendering and handles image cropping, scaling, and timing to ensure a consistent, full-screen experience.

## Project Overview

The program loads PNG images from a specified folder, randomizes their order, and cycles through a sequence: show the image, black screen for imagination, and rest (with optional "REST" text). It crops images to remove unwanted borders, scales them to fit the screen while preserving aspect ratio, and exports imagine phase timestamps to a CSV file in an `output` folder. This setup supports EEG data collection by providing precise timing for labeling brain signal data.

## Features

- **Randomized Image Sequence**: Loads and shuffles PNG files from a folder for unpredictable presentation.
- **Phased Display**: Configurable times for showing the image, imagination (black screen), and rest phases.
- **Image Processing**: Crops borders (e.g., black backgrounds) and scales images to fit full screen.
- **Timestamp Logging**: Records start and end times of the imagine phase for each image in a CSV file, formatted for easy alignment with EEG data.
- **Initial Countdown**: Starts with a black screen and console countdown for preparation.
- **Full-Screen Mode**: Uses Pygame for immersive, distraction-free display.
- **Output Management**: Automatically creates an `output` folder and generates timestamped CSV files.

## Installation and Setup

### Prerequisites

- Python 3.6+ (tested on Python 3.12)
- Pygame library for rendering graphics and handling display.

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Lo-Hei-Yip/Image-Sequence-Presenter.git
   cd Image-Sequence-Presenter
   ```

2. Install dependencies:

   ```bash
   pip install pygame
   ```

   The program also uses built-in Python modules: `os`, `random`, `csv`, and `datetime` (no additional installation needed).

3. Prepare images:

   - Place PNG files in a folder (e.g., `intermediate` or `advanced`) in the same directory as the script.
   - Ensure the folder exists and contains PNG images.

4. Run the program:

   ```bash
   python stimulus_presentation.py
   ```

   - The script will enter full-screen mode, display a countdown, run the sequence, and generate a CSV file in the `output` folder.
   - Press Ctrl+C in the terminal to exit early if needed (Pygame will quit gracefully).

**Note:** Run on a machine with a display. The program assumes PNG images are available; it raises an error if none are found.

## Customizable Variables

The program includes several variables at the top of the script (`stimulus_presentation.py`) for easy customization. Adjust them to fit your experimental needs:

- `folder = 'intermediate'`: The folder containing the PNG images. Change to `'advanced'` or any other folder name with your symbols (e.g., arrows like ↑, ↓).
- `show_time = 2`: Time to display each image (in seconds).
- `imagine_time = 2`: Duration of the imagine phase (black screen, in seconds). Timestamps for this phase are logged to CSV.
- `rest_total = 2`: Total rest time between trials (in seconds).
- `rest_text_time = 1`: Time to show "REST" text during rest (in seconds). Set to 0 to skip text and show only black screen.
- `crop_top = 1230`, `crop_bottom = 1230`, `crop_left = 3000`, `crop_right = 3000`: Pixels to crop from each side of the images (to remove black backgrounds or borders). Adjust based on your image dimensions to focus on the central content.
- `initial_black_screen_time = 3`: Initial black screen duration with console countdown (in seconds).

These variables control the timing, image processing, and folder input without modifying the core logic.

## How It Works

1. **Initialization**: Loads PNG images from the specified folder, shuffles them, and sets up Pygame for full-screen display.
2. **Countdown**: Shows a black screen with a console countdown to prepare the participant.
3. **Sequence Loop**:
   - **Show Phase**: Displays the cropped and scaled image centered on screen for `show_time` seconds.
   - **Imagine Phase**: Switches to black screen for `imagine_time` seconds, logging start/end timestamps.
   - **Rest Phase**: Shows "REST" text (if enabled) for `rest_text_time` seconds, followed by black screen for the remaining `rest_total` time.
4. **Output**: After all images, generates a CSV in the `output` folder with columns like `imagine_symbol_start_time` and `imagine_symbol_end_time` for each image (using filenames as identifiers). The CSV uses comma delimiters and includes a preview in the console.
5. **Cleanup**: Quits Pygame and prints a summary of processed images.

This structure ensures reliable stimulus presentation and timing for EEG synchronization, making it suitable for neuroscience experiments.

## Repository

Available at: [https://github.com/Lo-Hei-Yip/Image-Sequence-Presenter](https://github.com/Lo-Hei-Yip/Image-Sequence-Presenter)
