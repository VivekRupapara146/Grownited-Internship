import cv2
import numpy as np
from assets import *

CANVAS_W = 1920
CANVAS_H = 1080


# -------------------------------------------------
# BACKGROUND
# -------------------------------------------------

def create_steel_background(w=CANVAS_W, h=CANVAS_H):
    base_color = np.array([34,34,29], dtype=np.float32) #[25,28,32]

    y = np.linspace(0, 1, h)

    factors = np.where(
        y < 0.35,
        0.85 + (y / 0.35) * 0.1,
        np.where(
            y < 0.65,
            0.95 + ((y - 0.35) / 0.30) * 0.15,
            1.10 - ((y - 0.65) / 0.35) * 0.15
        )
    )

    gradient = (base_color[None, :] * factors[:, None])
    canvas = np.repeat(gradient[:, None, :], w, axis=1)

    return canvas.astype(np.uint8)


canvas = create_steel_background()


# -------------------------------------------------
# SIDE CAR
# -------------------------------------------------

side = preprocess_side(cv2.imread("CV_Project1\Pics\BMW-SideLook.jpg"))
sh, sw = side.shape[:2]

side_center_x = int(0.38 * CANVAS_W)
side_center_y = int(0.50 * CANVAS_H)

side_x = side_center_x - sw // 2
side_y = side_center_y - sh // 2

x1 = max(0, side_x)
y1 = max(0, side_y)
x2 = min(CANVAS_W, side_x + sw)
y2 = min(CANVAS_H, side_y + sh)

canvas[y1:y2, x1:x2] = np.maximum(
    canvas[y1:y2, x1:x2],
    side[y1 - side_y:y2 - side_y, x1 - side_x:x2 - side_x]
)


# -------------------------------------------------
# GHOST OUTLINE
# -------------------------------------------------

ghost, ghost_opacity = create_ghost_outline(
    cv2.imread("CV_Project1\Pics\BMW-SideLook.jpg"),
    opacity=0.3
)

ghost = tint_eyes_custom(ghost)

gh, gw = ghost.shape[:2]

ghost_center_x = int(0.636 * CANVAS_W)
ghost_center_y = int(0.44 * CANVAS_H)

gx = ghost_center_x - gw // 2
gy = ghost_center_y - gh // 2

x1 = max(gx, 0)
y1 = max(gy, 0)
x2 = min(gx + gw, CANVAS_W)
y2 = min(gy + gh, CANVAS_H)

ghost_crop = ghost[y1 - gy:y2 - gy, x1 - gx:x2 - gx]
roi = canvas[y1:y2, x1:x2]

canvas[y1:y2, x1:x2] = cv2.addWeighted(
    roi, 1.0,
    ghost_crop, ghost_opacity,
    0
)


# -------------------------------------------------
# HERO
# -------------------------------------------------

hero = preprocess_hero(cv2.imread("CV_Project1\Pics\BM-M4.jpg"))

hh, hw = hero.shape[:2]

center_x = int(0.55 * CANVAS_W)
center_y = int(0.48 * CANVAS_H) + 25

top_left_x = center_x - hw // 2
top_left_y = center_y - hh // 2

canvas[top_left_y:top_left_y+hh,
       top_left_x:top_left_x+hw] = hero


# -------------------------------------------------
# EYES
# -------------------------------------------------

left_eye, right_eye = extractRightEye(
    cv2.imread("CV_Project1\Pics\BM-M4_CrossLook.jpg")
)

eye_h, eye_w = left_eye.shape[:2]
gap = 30
combined_w = eye_w * 2 + gap

# Darken top hero once
hero[:250] = (hero[:250] * 0.35).astype(np.uint8)

eyes_pair = np.zeros((eye_h, combined_w, 3), dtype=np.uint8)
eyes_pair[:, :eye_w] = left_eye
eyes_pair[:, eye_w + gap:combined_w] = right_eye

eyes_pair = np.clip(eyes_pair * 1.4, 0, 255).astype(np.uint8) # brighten

sharpen_kernel = np.array([[0,-1,0],
                           [-1,5,-1],
                           [0,-1,0]])

eyes_combined = cv2.filter2D(eyes_pair, -1, sharpen_kernel)
eyes_combined = tint_eyes_custom(eyes_combined, color=(0,255,255))

eyes_y = max(0, top_left_y - 60)
eyes_left_x = max(0, center_x - combined_w // 2)

canvas[eyes_y:eyes_y+eye_h,
       eyes_left_x:eyes_left_x+combined_w] = np.maximum(
    canvas[eyes_y:eyes_y+eye_h,
           eyes_left_x:eyes_left_x+combined_w],
    eyes_combined
)

# -------------------------------------------------
# TOP LEFT IMAGE
# -------------------------------------------------

img = darken_image(cv2.imread("CV_Project1\Pics\BM-M4_CrossLook.jpg"), 0.8)

canvas, img_resized = add_top_left_image(
    canvas,
    img,
    scale_ratio=0.38
)


# -------------------------------------------------
# TOP RIGHT BADGE
# -------------------------------------------------

canvas = add_top_right_image(
    canvas,
    cv2.imread("CV_Project1\Pics\BMW-Logo_3.jpg"),
    margin=40,
    blend_mode="overwrite"
)


# -------------------------------------------------
# BOTTOM LEFT LOGO
# -------------------------------------------------

logo = darken_image(cv2.imread("CV_Project1\Pics\BMW-Logo_2.jpg"), 1.0)

canvas = add_image(
    canvas,
    logo,
    x_ref=40,
    y_ref=CANVAS_H - 40 - 340,
    target_w=280,
    target_h=300,
    x_anchor="left",
    y_anchor="top",
    blend_mode="maximum",
    opacity=0.8
)

# -------------------------------------------------
# BOTTOM RIGHT IMAGE
# -------------------------------------------------
logo2 = cv2.flip(cv2.imread("CV_Project1\Pics\BMW-Logo.jpg"),1)
logo2, logo2_opacity = create_ghost_outline(logo2)
canvas = add_image(
    canvas,
    logo2,
    x_ref=CANVAS_W - 40,
    y_ref=CANVAS_H - 40 - 340,
    target_w=250,
    target_h=300,
    x_anchor="right",
    y_anchor="top",
    blend_mode="maximum",
    opacity=0.8
)

# -------------------------------------------------
# FINAL SHADING
# -------------------------------------------------

canvas = apply_center_shading(canvas, strength=0.20)


# -------------------------------------------------
# OUTPUT
# -------------------------------------------------

cv2.imwrite("CV_Project1\Poster.jpg", canvas)

cv2.imshow("Poster", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
