# 🚗 BMW M4 Cinematic Poster Generator

A fully programmatic cinematic poster generator built using **OpenCV + NumPy**.

This project creates a high-resolution (1920×1080) BMW M4 automotive poster through layered compositing, gradient lighting, headlight extraction, ghost outline effects, and modular image placement—**all without external design tools**.

Everything is generated through algorithmic image processing.

---

## 🎯 Project Goal

Design a cinematic automotive poster entirely using:

- **OpenCV** image processing
- **NumPy** vectorized operations
- **Layered compositing** logic
- **Controlled color grading**
- **Procedural lighting** effects

**No Photoshop. No deep learning. Pure OpenCV.**

---

## 🖼️ Final Output Features

✨ **Visual Elements:**

- Steel-tone cinematic gradient background
- Dominant hero car with top exposure fade
- Darkened side car for depth layering
- Extracted & stylized headlight "eyes"
- Ghost wireframe outline overlay
- Modular top-left and top-right image placement
- Logo compositing with transparency
- Radial spotlight shading
- Multiple blend modes (overwrite / maximum / blend)

---

## 🏗️ Architecture Overview

The project is structured into two main files:
```
main.py     → Poster composition pipeline
assets.py   → Reusable image-processing functions
```

**Design Philosophy:** Modular, reusable, and fully parameterized for easy customization.

---

## 🧠 Processing Pipeline

### **1️⃣ Background Creation**

- 3-tone vertical steel gradient
- Fully vectorized (no Python loops)
- Cinematic contrast control for professional look

### **2️⃣ Hero Car Processing**

- Proportional canvas fit with aspect ratio preservation
- Portrait-safe vertical crop to prevent distortion
- Height-controlled scaling for consistent sizing
- Top fade for headlight visibility enhancement
- Optional bottom fade for grounding effect
- Controlled darkening for mood and atmosphere

### **3️⃣ Side Car Processing**

- Canvas-safe resizing with boundary checks
- Front-section crop focusing on key features
- Desaturation for depth layering (prevents visual competition)
- Left-edge cinematic fade for seamless integration
- Slight rotation for dynamic motion effect

### **4️⃣ Eye (Headlight) Extraction & Styling**

- **HSV threshold** for white headlight isolation
- Proportional resize to fit poster dimensions
- Mirroring for left/right symmetry
- Inward tilt rotation for aggressive look
- Sharpening filter for crisp detail
- Brightness boost for prominence
- Custom tinting with BGR-based color control
- Intelligent eye-pair compositing

### **5️⃣ Ghost Outline Effect**

- Grayscale conversion for edge detection
- Gaussian blur for noise reduction
- **Canny edge detection** for precise outlines
- Line dilation for visibility
- Opacity blending for subtle effect
- Cropped positioning for artistic framing

### **6️⃣ Modular Image Placement System**

**Reusable placement functions:**

- `add_top_left_image()` - Top-left corner placement
- `add_top_right_image()` - Top-right corner placement
- `add_image()` - Custom position placement

**Features:**

- **Horizontal anchors:** `left`, `center`, `right`
- **Vertical anchors:** `top`, `center`, `bottom`
- Safe boundary clipping (prevents overflow)
- **Blend modes:**
  - `overwrite` - Direct replacement
  - `maximum` - Brighten-only composite
  - `blend` - Alpha-based transparency
- Opacity control (0.0 to 1.0)

### **7️⃣ Radial Center Shading**

Cinematic spotlight effect:

- Bright center focus
- Darker edges for vignette
- Adjustable intensity for mood control

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.x** | Core programming language |
| **OpenCV (cv2)** | Image processing and compositing |
| **NumPy** | Vectorized array operations |

**No external compositing libraries. No GPU acceleration. No deep learning.**

---

## 🚀 How to Run

### **Installation**
```bash
pip install opencv-python numpy
```

### **Execution**
```bash
python main.py
```

### **Output**

Generated file: `Stage6.jpg` (1920×1080 resolution)

---

## 🎨 Customization Guide

### **Change Eye (Headlight) Color**
```python
tint_eyes_custom(eyes_combined, color=(0, 255, 255))  # BGR format
```

**Color examples:**
- `(0, 255, 255)` → Yellow/Gold
- `(255, 0, 0)` → Blue
- `(0, 0, 255)` → Red
- `(0, 255, 0)` → Green

### **Adjust Hero Car Position**
```python
center_x = int(0.55 * CANVAS_W)  # Horizontal: 0.0 (left) to 1.0 (right)
center_y = int(0.48 * CANVAS_H)  # Vertical: 0.0 (top) to 1.0 (bottom)
```

### **Adjust Spotlight Strength**
```python
apply_center_shading(canvas, strength=0.75)
```

**Strength guide:**
- `0.3` → Subtle, natural lighting
- `0.6` → Cinematic, professional look
- `0.8+` → Dramatic, high-contrast effect

### **Adjust Ghost Outline Opacity**
```python
create_ghost_outline(..., opacity=0.3)
```

**Range:** `0.0` (invisible) to `1.0` (fully visible)

### **Modify Background Gradient**
```python
# In assets.py - modify gradient_bg() function
colors = [(40, 50, 60), (60, 70, 80), (80, 90, 100)]  # Dark to light
```

---

## 📈 Optimization Highlights

✅ **Performance optimizations:**

- Vectorized gradient generation (no loops)
- Reduced redundant memory operations
- Efficient alpha masking strategy
- Modular reusable functions
- Safe ROI (Region of Interest) clipping
- Minimal unnecessary array copies
- In-place operations where possible

---

## 🧩 Design Principles

**Core techniques applied:**

- **Layer-based compositing** - Professional multi-layer workflow
- **Subject isolation** through selective desaturation
- **Controlled exposure gradients** for cinematic mood
- **Depth creation** via fade masks and opacity
- **Cinematic lighting simulation** with radial shading
- **Parameterized styling system** for flexibility
- **Non-destructive editing** through function composition

---

## 🔮 Possible Enhancements

**Future feature ideas:**

- [ ] Layer management system with Z-index control
- [ ] Automatic layout presets (grid, rule of thirds, golden ratio)
- [ ] Batch poster generator for multiple cars
- [ ] Motion blur effects for speed sensation
- [ ] LUT-based color grading (cinematic color profiles)
- [ ] Animation export (video sequence generation)
- [ ] GUI interface for real-time tuning
- [ ] Text overlay system (titles, captions, branding)
- [ ] HDR tone mapping
- [ ] Lens flare effects
- [ ] Particle system (dust, rain, sparks)

---

## 📌 Educational Value

**This project demonstrates:**

| Concept | Application |
|---------|-------------|
| **Advanced OpenCV compositing** | Multi-layer image blending |
| **Gradient mask construction** | Procedural fade effects |
| **HSV thresholding** | Color-based object isolation |
| **Edge-based styling** | Canny detection & outline effects |
| **Geometric transforms** | Rotation, scaling, cropping |
| **Procedural lighting design** | Radial gradients & shading |
| **Modular architecture** | Reusable function library |
| **Vectorized operations** | NumPy optimization techniques |

---

## 📂 Project Structure
```
bmw-poster-generator/
│
├── main.py              # Main composition pipeline
├── assets.py            # Reusable processing functions
├── images/              # Input images directory
│   ├── hero_car.jpg
│   ├── side_car.jpg
│   ├── logo.png
│   └── ...
└── Stage6.jpg          # Generated output poster
```

---

## 🎓 Learning Outcomes

**Skills developed:**

✅ Understanding of compositing fundamentals  
✅ Mastery of OpenCV image manipulation  
✅ Practical application of color theory  
✅ Implementation of blend modes  
✅ Creation of procedural effects  
✅ Optimization of image processing pipelines  
✅ Modular software architecture design  

---

## 📝 License

This project is open-source and available for educational purposes.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](#) for known problems or suggestions.

---

## 👨‍💻 Author

**Vivek Rupapara**

- GitHub: VivekRupapara146
- Email: vivek.rupapara.g@gmail.com

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you learn image processing techniques!

---

## 🙏 Acknowledgments

- BMW for automotive design inspiration
- OpenCV community for comprehensive documentation
- Computer vision researchers for algorithmic foundations

---

**Built with ❤️ using OpenCV and NumPy**
