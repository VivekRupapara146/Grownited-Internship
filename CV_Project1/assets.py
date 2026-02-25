import cv2
import numpy as np

CANVAS_W = 1920
CANVAS_H = 1080


# -------------------------------------------------
# BASIC UTIL
# -------------------------------------------------

def darken_image(img, factor=0.6):
    return np.clip(img.astype(np.float32) * factor, 0, 255).astype(np.uint8)


# -------------------------------------------------
# HERO PREPROCESS
# -------------------------------------------------

def preprocess_hero(img, canvas_w=CANVAS_W, canvas_h=CANVAS_H, target_h=850):

    h, w = img.shape[:2]

    # Fit to canvas
    scale = min(canvas_w / w, canvas_h / h, 1.0)
    resized = cv2.resize(img, (int(w * scale), int(h * scale)))

    # Dynamic crop
    h2 = resized.shape[0]
    cropped = resized[int(0.12 * h2):int(0.98 * h2), :]

    # Height-based resize
    ch, cw = cropped.shape[:2]
    scale2 = min(target_h / ch, 1.0)
    final = cv2.resize(cropped, (int(cw * scale2), int(ch * scale2)))

    # Darken slightly
    final = darken_image(final,factor=0.85)

    # Top fade
    fh, fw = final.shape[:2]
    fade_height = int(0.30 * fh)

    gradient = np.linspace(0.20, 1.0, fade_height, dtype=np.float32)
    fade_mask = np.ones((fh, fw), dtype=np.float32)
    fade_mask[:fade_height] = gradient[:, None]
    # final = (final * np.dstack([fade_mask]*3)).astype(np.uint8)

    # Bottom Fade
    gradient2 = np.linspace(1.0, 0.20, fade_height, dtype=np.float32)
    fade_mask2 = np.ones((fh, fw), dtype=np.float32)
    fade_mask2[fh-fade_height:]= gradient2[:,None]
    # final = (final * np.dstack([fade_mask2]*3)).astype(np.uint8)
    combined_mask = fade_mask * fade_mask2
    final = (final * np.dstack([combined_mask]*3)).astype(np.uint8)

    return final


# -------------------------------------------------
# SIDE PREPROCESS
# -------------------------------------------------

def preprocess_side(img, canvas_w=CANVAS_W, canvas_h=CANVAS_H,
                    target_w=1200, dark_factor=0.70,
                    rotate_angle=-8):

    h, w = img.shape[:2]

    # Fit safely
    scale = min(canvas_w / w, canvas_h / h)
    resized = cv2.resize(img, (int(w * scale), int(h * scale)))

    # Crop front
    resized = resized[:, :int(0.8 * resized.shape[1])]

    # Resize to target width
    ch, cw = resized.shape[:2]
    scale2 = target_w / cw
    resized = cv2.resize(resized, (target_w, int(ch * scale2)))

    # Darken
    resized = (resized * dark_factor).astype(np.uint8)

    # Desaturate
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = (hsv[..., 1] * 0.7).astype(np.uint8)
    resized = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Left fade
    fh, fw = resized.shape[:2]
    fade_w = int(0.35 * fw)

    gradient = np.linspace(0, 1, fade_w, dtype=np.float32)
    fade_mask = np.ones((fh, fw), dtype=np.float32)
    fade_mask[:, :fade_w] = gradient

    resized = (resized * np.dstack([fade_mask]*3)).astype(np.uint8)

    # Rotate
    M = cv2.getRotationMatrix2D((fw // 2, fh // 2), rotate_angle, 1.3)
    rotated = cv2.warpAffine(
        resized, M, (fw, fh),
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0)
    )

    return rotated


# -------------------------------------------------
# EYE EXTRACTION
# -------------------------------------------------

def extractRightEye(img, target_w=262, tilt_angle=-10):

    cropped = img[450:800, 850:1390]

    hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 0, 250]), np.array([180, 45, 255]))

    result = np.zeros_like(cropped)
    result[mask == 255] = [220, 220, 220]

    h, w = result.shape[:2]
    resized = cv2.resize(result, (int(w * (target_w / w)), 160))

    left_eye = cv2.flip(resized, 1)
    right_eye = resized

    def rotate_with_bound(image, angle):
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        cos = abs(M[0, 0])
        sin = abs(M[0, 1])

        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]

        return cv2.warpAffine(image, M, (new_w, new_h))

    return rotate_with_bound(left_eye, tilt_angle), \
           rotate_with_bound(right_eye, -tilt_angle)


# -------------------------------------------------
# GHOST OUTLINE
# -------------------------------------------------

def create_ghost_outline(img, scale_factor=1.0, opacity=0.18):

    h, w = img.shape[:2]
    img_big = cv2.resize(img, (int(w * scale_factor), int(h * scale_factor)))

    M = cv2.getRotationMatrix2D(
        (img_big.shape[1]//2, img_big.shape[0]//2),
        -6, 1.0
    )
    rotated = cv2.warpAffine(img_big, M,
                             (img_big.shape[1], img_big.shape[0]))

    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    edges = cv2.Canny(blur, 80, 160)

    edges = cv2.dilate(edges, np.ones((2,2), np.uint8), iterations=1)

    ghost = np.zeros_like(rotated)
    ghost[edges > 0] = [255,255,255]

    gh, gw = ghost.shape[:2]
    ghost = ghost[:int(0.85*gh), int(0.32*gw):]

    return ghost, opacity


# -------------------------------------------------
# IMAGE PLACEMENT
# -------------------------------------------------

def add_top_right_image(canvas, img, margin=40, blend_mode="overwrite"):

    img = cv2.resize(img, (530, 250))
    h, w = img.shape[:2]
    canvas_h, canvas_w = canvas.shape[:2]

    x1 = canvas_w - margin - w
    y1 = margin
    x2 = x1 + w
    y2 = y1 + h

    if x1 < 0 or y1 < 0 or x2 > canvas_w or y2 > canvas_h:
        return canvas

    roi = canvas[y1:y2, x1:x2]

    if blend_mode == "overwrite":
        canvas[y1:y2, x1:x2] = img
    elif blend_mode == "maximum":
        canvas[y1:y2, x1:x2] = np.maximum(roi, img)
    elif blend_mode == "blend":
        canvas[y1:y2, x1:x2] = cv2.addWeighted(roi, 0.7, img, 0.3, 0)

    return canvas


# -------------------------------------------------
# CENTER SHADING
# -------------------------------------------------

def apply_center_shading(canvas, strength=0.4):

    h, w = canvas.shape[:2]

    y, x = np.ogrid[:h, :w]
    center_x, center_y = w // 2, h // 2

    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    max_dist = np.sqrt(center_x**2 + center_y**2)

    mask = 1 - (distance / max_dist * strength)
    mask = np.clip(mask, 0.3, 1.0)

    return (canvas * np.dstack([mask]*3)).astype(np.uint8)

# Recoloring Eyes

def tint_eyes_custom(img, color=(180, 130, 70)):
    """
    color = (B, G, R)
    Example steel blue: (180,130,70)
    """

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Create mask for bright pixels (white lines)
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Create empty colored image
    colored = np.zeros_like(img)

    # Apply custom color only where mask is white
    colored[mask == 255] = color

    return colored

def add_top_left_image(canvas, img, canvas_w = 1920, scale_ratio = 0.35, margin = 40, opacity = 1.0):
    
    if img is None:
        return canvas
    # Resize
    h, w = img.shape[:2]
    target_w = int(scale_ratio * canvas_w)
    scale = target_w / w
    new_w = target_w
    new_h = int(h * scale)

    img_resize = cv2.resize(cv2.flip(img, 1), (new_w, new_h))
    # darker resize
    img_resize = np.clip(img_resize * 0.65, 0, 255).astype(np.uint8)

    dh, dw = img_resize.shape[:2]

    x = margin
    y = margin

    # Prevent overflow
    canvas_h, canvas_w = canvas.shape[:2]
    if x + dw > canvas_w or y + dh > canvas_h:
        return canvas

    roi = canvas[y:y+dh, x:x+dw]

    if opacity < 1.0:
        blended = cv2.addWeighted(roi, 1.0 - opacity, img_resize, opacity, 0)
        canvas[y:y+dh, x:x+dw] = blended
    else:
        canvas[y:y+dh, x:x+dw] = img_resize

    return canvas , img_resize

def add_image(canvas, img,
              x_ref, y_ref, target_w, target_h,
              x_anchor="left",
              y_anchor="top",
              
              blend_mode="overwrite",
              opacity=1.0):
    """
    Places image on canvas WITHOUT resizing.

    x_ref, y_ref  → reference point on canvas
    x_anchor      → 'left', 'center', 'right'
    y_anchor      → 'top', 'center', 'bottom'
    blend_mode    → 'overwrite', 'maximum', 'blend'
    opacity       → used only in 'blend' mode
    """

    img = cv2.resize(img,(target_w, target_h))
    h, w = img.shape[:2]
    canvas_h, canvas_w = canvas.shape[:2]

    # --- Horizontal alignment ---
    if x_anchor == "left":
        x = x_ref + 15
    elif x_anchor== "center":
        x = x_ref - w // 2
    elif x_anchor == "right":
        x = x_ref - w - 10
    else:
        raise ValueError("Invalid x_anchor")

    # --- Vertical alignment ---
    if y_anchor == "top":
        y = y_ref
    elif y_anchor == "center":
        y = y_ref - h // 2
    elif y_anchor == "bottom":
        y = y_ref - h
    else:
        raise ValueError("Invalid y_anchor")

    # --- Boundary Safe Placement ---
    x1 = max(x, 0)
    y1 = max(y, 0)
    x2 = min(x + w, canvas_w)
    y2 = min(y + h, canvas_h)

    if x1 >= x2 or y1 >= y2:
        return canvas  # nothing visible

    img_x1 = x1 - x
    img_y1 = y1 - y
    img_x2 = img_x1 + (x2 - x1)
    img_y2 = img_y1 + (y2 - y1)

    roi = canvas[y1:y2, x1:x2]
    img_crop = img[img_y1:img_y2, img_x1:img_x2]

    # --- Blend Modes ---
    if blend_mode == "overwrite":
        canvas[y1:y2, x1:x2] = img_crop

    elif blend_mode == "maximum":
        canvas[y1:y2, x1:x2] = np.maximum(roi, img_crop)

    elif blend_mode == "blend":
        blended = cv2.addWeighted(
            roi, 1 - opacity,
            img_crop, opacity,
            0
        )
        canvas[y1:y2, x1:x2] = blended

    else:
        raise ValueError("Invalid blend_mode")

    return canvas