# VespoUAV ArUco Marker Generator

A Python script to generate and save ArUco markers for the VespoUAV autonomous drone team. This tool creates customizable 5x5 ArUco markers following TMR (Torneo Mexicano de Robótica) specifications.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

---

## Requirements

- **Python 3.7 or higher**
- **OpenCV (cv2)** with ArUco support
- **Operating System:** Linux, macOS, or Windows
- **Disk Space:** At least 100 MB for generated markers

---

## Installation

### Step 1: Install Python Dependencies

First, ensure you have `pip` installed. Then run:

```bash
pip install opencv-python opencv-contrib-python
```

Verify the installation:

```bash
python3 -c "import cv2; import cv2.aruco; print('OpenCV version:', cv2.__version__)"
```

### Step 2: Clone or Download the Repository

Navigate to your workspace:

```bash
cd /data/workspace_aruco/src/aruco_detector_pkg
```

Ensure the script is in the `scripts/` directory:

```bash
ls scripts/aruco_generator.py
```

### Step 3: Make the Script Executable

```bash
chmod +x scripts/aruco_generator.py
```

---

## Usage

### Running the Script

From the root of the `aruco_detector_pkg` directory, run:

```bash
./scripts/aruco_generator.py
```

Or alternatively:

```bash
python3 scripts/aruco_generator.py
```

### Interactive Menu

The script will present you with four questions:

#### **Question 1: How many markers do you want to generate?**
- Enter a number between **1 and 100**
- Example: `5` (generates 5 markers)

#### **Question 2: What size do you want the markers to be (in pixels)?**
- Enter the desired size in pixels
- Example: `200` (creates 200x200 pixel markers)
- **Recommendation:** Use sizes between 100-300 pixels for Gazebo simulation

#### **Question 3: Do you want the markers to be consecutive?**
- Type `y` for **yes** (generates markers 0, 1, 2, ...)
- Type `n` for **no** (specify exact IDs)

#### **Option A: Consecutive Markers (if you chose 'y')**
- Markers are generated with consecutive IDs starting from 0
- Example: If you chose 5 markers, it generates IDs: 0, 1, 2, 3, 4

#### **Option B: Specific Marker IDs (if you chose 'n')**
- You will be prompted to enter specific marker IDs separated by commas
- Example: `5,12,47,88,99` (generates exactly those 5 markers)

**Validation Rules:**
- All marker IDs must be between 0 and 99
- Duplicate IDs are not allowed
- The number of IDs must match the number you specified in Question 1

### Output

Once generated, all markers are saved as PNG images in:

```
models/aruco_markers/textures/aruco_[ID].png
```

Example output:
```
Marker 0 generated and saved as .../aruco_0.png
Marker 1 generated and saved as .../aruco_1.png
Marker 2 generated and saved as .../aruco_2.png
...
```

---

## Project Structure

```
aruco_detector_pkg/
├── scripts/
│   └── aruco_generator.py          # Main script (this file)
├── models/
│   └── aruco_markers/
│       └── textures/               # Generated PNG markers (created automatically)
│           ├── aruco_0.png
│           ├── aruco_1.png
│           └── ...
├── launch/
├── worlds/
└── README.md
```

---

## Features

### Implemented Features

- **Interactive CLI Menu** - User-friendly command-line interface with colored output
- **Flexible Marker Generation** - Generate consecutive or specific marker IDs
- **Input Validation** - Comprehensive error checking for user input
- **Automatic Directory Creation** - Creates output directories if they don't exist
- **Visual Preview** - Displays a sample ArUco marker in the terminal at startup
- **Error Handling** - Graceful handling of invalid inputs with retry prompts
- **Duplicate Detection** - Prevents duplicate marker IDs from being specified
- **TMR Compliance** - Uses 5x5 ArUco dictionary as per TMR regulations

### Specifications

- **ArUco Dictionary:** `DICT_5X5_100` (100 unique markers, 5x5 grid pattern)
- **Supported Marker IDs:** 0 to 99
- **Output Format:** PNG images (white background, black pattern)
- **Customizable:** Marker size and quantity

---

## Examples

### Example 1: Generate 5 consecutive markers (200x200 pixels)

```
How many markers do you want to generate? (1-100): 5
What size do you want the markers to be? (in pixels): 200
Do you want the markers to be consecutive? (y/n): y
```

**Result:** Generates `aruco_0.png`, `aruco_1.png`, ... `aruco_4.png` (200x200 pixels each)

### Example 2: Generate 3 specific markers (150x150 pixels)

```
How many markers do you want to generate? (1-100): 3
What size do you want the markers to be? (in pixels): 150
Do you want the markers to be consecutive? (y/n): n
Please enter the specific marker IDs: 10,25,88
```

**Result:** Generates `aruco_10.png`, `aruco_25.png`, `aruco_88.png` (150x150 pixels each)

### Example 3: Error Handling - Invalid Input

```
Please enter the specific marker IDs: 5,5,10
Error: Duplicate marker IDs are not allowed.
Please enter the specific marker IDs: 5,10,15
```

---

## Troubleshooting

### Issue: `bash: ./scripts/aruco_generator.py: /user/bin/env: bad interpreter: No such file or directory`

**Solution:** The shebang line has a typo. Fix it:

```bash
sed -i 's|#!/user/bin/env|#!/usr/bin/env|g' scripts/aruco_generator.py
```

Then try again:

```bash
./scripts/aruco_generator.py
```

---

### Issue: `ModuleNotFoundError: No module named 'cv2'`

**Solution:** Install OpenCV:

```bash
pip install opencv-python opencv-contrib-python
```

---

### Issue: `Permission denied` when running the script

**Solution:** Make the script executable:

```bash
chmod +x scripts/aruco_generator.py
```

---

### Issue: Generated markers not found in the textures directory

**Solution:** Verify the directory was created:

```bash
ls -la models/aruco_markers/textures/
```

If the directory doesn't exist, the script should create it automatically. If not, create it manually:

```bash
mkdir -p models/aruco_markers/textures
```

---

## Advanced Usage

### Programmatic Usage (in your own Python code)

```python
import cv2.aruco as aruco
from pathlib import Path

# Get the ArUco dictionary
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)

# Generate a single marker
img = aruco.generateImageMarker(aruco_dict, marker_id=5, sidePixels=200)

# Save it
cv2.imwrite("my_marker.png", img)
```

---

## Technical Details

### ArUco 5x5 Specification

- **Grid Size:** 5 bits × 5 bits (25 bits total)
- **Dictionary:** DICT_5X5_100 (supports 100 unique markers)
- **Valid IDs:** 0 to 99
- **Use Case:** Medium-range detection (1-3 meters typical)
- **Standards Compliance:** OpenCV ArUco module, TMR regulations

## References

- [OpenCV ArUco Documentation](https://docs.opencv.org/master/d5/dae/tutorial_aruco_detection.html)
- [TMR Torneo Mexicano de Robótica](https://femexrobotica.org/tmr2026/)

---

## License

This project is part of the VespoUAV autonomous drone team at Tecnológico de Monterrey, Campus Estado de México.

---

## Author

**Imad Jared Cabrera Trejo**  
Team Leader - VespoUAV  
Contact: cabreratrejoimadjared@gmail.com

---

## Support

For issues, questions, or suggestions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [Usage](#usage) examples
3. Contact the development team

---