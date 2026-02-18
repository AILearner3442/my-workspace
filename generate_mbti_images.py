#!/usr/bin/env python3
"""Generate MBTI character illustrations using PIL"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

OUTPUT_DIR = "content/images"
WIDTH, HEIGHT = 800, 1000

def create_gradient(draw, width, height, color1, color2, vertical=True):
    """Create a gradient background"""
    for i in range(height if vertical else width):
        ratio = i / (height if vertical else width)
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        if vertical:
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, height)], fill=(r, g, b))

def draw_person_base(draw, x, y, skin_color, hair_color, scale=1.0):
    """Draw base person shape (head and body)"""
    # Head
    head_radius = int(60 * scale)
    draw.ellipse([x - head_radius, y - head_radius, x + head_radius, y + head_radius],
                 fill=skin_color, outline=skin_color)

    # Hair
    hair_points = []
    for angle in range(180, 361):
        rad = math.radians(angle)
        px = x + int((head_radius + 5) * math.cos(rad) * scale)
        py = y + int((head_radius + 5) * math.sin(rad) * scale)
        hair_points.append((px, py))
    if len(hair_points) > 2:
        draw.polygon(hair_points, fill=hair_color)

    # Simple hair on top
    draw.ellipse([x - head_radius - 5, y - head_radius - 15, x + head_radius + 5, y - 10],
                 fill=hair_color)

    return head_radius

def draw_eyes(draw, x, y, eye_color=(50, 50, 50), scale=1.0):
    """Draw simple eyes"""
    eye_offset_x = int(20 * scale)
    eye_offset_y = int(-5 * scale)
    eye_radius = int(8 * scale)

    # Left eye
    draw.ellipse([x - eye_offset_x - eye_radius, y + eye_offset_y - eye_radius,
                  x - eye_offset_x + eye_radius, y + eye_offset_y + eye_radius],
                 fill=(255, 255, 255))
    draw.ellipse([x - eye_offset_x - eye_radius//2, y + eye_offset_y - eye_radius//2,
                  x - eye_offset_x + eye_radius//2, y + eye_offset_y + eye_radius//2],
                 fill=eye_color)

    # Right eye
    draw.ellipse([x + eye_offset_x - eye_radius, y + eye_offset_y - eye_radius,
                  x + eye_offset_x + eye_radius, y + eye_offset_y + eye_radius],
                 fill=(255, 255, 255))
    draw.ellipse([x + eye_offset_x - eye_radius//2, y + eye_offset_y - eye_radius//2,
                  x + eye_offset_x + eye_radius//2, y + eye_offset_y + eye_radius//2],
                 fill=eye_color)

def draw_smile(draw, x, y, scale=1.0):
    """Draw a simple smile"""
    smile_y = int(25 * scale)
    draw.arc([x - 20, y + smile_y - 15, x + 20, y + smile_y + 15],
             start=0, end=180, fill=(180, 100, 100), width=3)

def draw_glasses(draw, x, y, scale=1.0, color=(40, 40, 40)):
    """Draw rectangular glasses"""
    eye_offset_x = int(20 * scale)
    eye_offset_y = int(-5 * scale)
    glass_w = int(25 * scale)
    glass_h = int(18 * scale)

    # Left lens
    draw.rectangle([x - eye_offset_x - glass_w, y + eye_offset_y - glass_h,
                    x - eye_offset_x + glass_w, y + eye_offset_y + glass_h],
                   outline=color, width=3)

    # Right lens
    draw.rectangle([x + eye_offset_x - glass_w, y + eye_offset_y - glass_h,
                    x + eye_offset_x + glass_w, y + eye_offset_y + glass_h],
                   outline=color, width=3)

    # Bridge
    draw.line([x - eye_offset_x + glass_w, y + eye_offset_y,
               x + eye_offset_x - glass_w, y + eye_offset_y], fill=color, width=3)

def generate_intj():
    """INTJ: Deep blue-purple background + person with glasses in formal attire"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # Deep blue-purple gradient background
    create_gradient(draw, WIDTH, HEIGHT, (20, 20, 60), (60, 20, 80))

    # Add some geometric patterns (INTJ likes structure)
    for i in range(5):
        y_pos = 150 + i * 180
        draw.line([(50, y_pos), (750, y_pos)], fill=(80, 60, 120, 50), width=1)

    # Draw person
    center_x, center_y = WIDTH // 2, 350
    skin_color = (255, 220, 185)
    hair_color = (40, 30, 30)

    # Body (formal suit)
    suit_color = (30, 30, 50)
    # Shoulders and torso
    draw.polygon([(center_x - 120, center_y + 80),
                  (center_x + 120, center_y + 80),
                  (center_x + 150, center_y + 400),
                  (center_x - 150, center_y + 400)], fill=suit_color)

    # Collar / shirt
    draw.polygon([(center_x - 30, center_y + 80),
                  (center_x + 30, center_y + 80),
                  (center_x + 15, center_y + 160),
                  (center_x - 15, center_y + 160)], fill=(240, 240, 250))

    # Tie
    draw.polygon([(center_x - 15, center_y + 110),
                  (center_x + 15, center_y + 110),
                  (center_x + 8, center_y + 250),
                  (center_x - 8, center_y + 250)], fill=(100, 50, 50))

    # Arms
    draw.polygon([(center_x - 120, center_y + 80),
                  (center_x - 150, center_y + 300),
                  (center_x - 100, center_y + 300),
                  (center_x - 80, center_y + 120)], fill=suit_color)

    draw.polygon([(center_x + 120, center_y + 80),
                  (center_x + 150, center_y + 300),
                  (center_x + 100, center_y + 300),
                  (center_x + 80, center_y + 120)], fill=suit_color)

    # Head
    draw_person_base(draw, center_x, center_y, skin_color, hair_color)
    draw_eyes(draw, center_x, center_y, (30, 30, 50))
    draw_glasses(draw, center_x, center_y)

    # Serious expression (straight line)
    draw.line([center_x - 15, center_y + 30, center_x + 15, center_y + 30],
              fill=(180, 120, 120), width=3)

    # INTJ label
    draw.rectangle([WIDTH//2 - 80, HEIGHT - 120, WIDTH//2 + 80, HEIGHT - 60],
                   fill=(60, 40, 100), outline=(120, 100, 180), width=3)
    # Text
    draw.text((WIDTH//2 - 40, HEIGHT - 110), "INTJ", fill=(220, 220, 255))

    img.save(os.path.join(OUTPUT_DIR, "mbti_intj.png"))
    print("Generated mbti_intj.png")

def generate_enfp():
    """ENFP: Orange-pink gradient + lively person with hands raised"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # Orange-pink gradient background
    create_gradient(draw, WIDTH, HEIGHT, (255, 150, 100), (255, 120, 180))

    # Add fun sparkles/circles
    import random
    random.seed(42)
    for _ in range(30):
        cx = random.randint(50, WIDTH - 50)
        cy = random.randint(50, HEIGHT - 50)
        r = random.randint(5, 20)
        alpha = random.randint(100, 200)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(255, 255, 255))

    # Draw person
    center_x, center_y = WIDTH // 2, 380
    skin_color = (255, 210, 180)
    hair_color = (255, 180, 100)

    # Colorful casual outfit
    outfit_color = (255, 200, 100)

    # Body
    draw.polygon([(center_x - 80, center_y + 80),
                  (center_x + 80, center_y + 80),
                  (center_x + 100, center_y + 350),
                  (center_x - 100, center_y + 350)], fill=outfit_color)

    # Pattern on outfit
    for i in range(5):
        y_stripe = center_y + 120 + i * 50
        draw.line([(center_x - 70, y_stripe), (center_x + 70, y_stripe)],
                  fill=(255, 100, 150), width=8)

    # Arms raised up excitedly!
    # Left arm up
    draw.polygon([(center_x - 80, center_y + 80),
                  (center_x - 150, center_y - 100),
                  (center_x - 100, center_y - 120),
                  (center_x - 60, center_y + 60)], fill=skin_color)

    # Right arm up
    draw.polygon([(center_x + 80, center_y + 80),
                  (center_x + 150, center_y - 100),
                  (center_x + 100, center_y - 120),
                  (center_x + 60, center_y + 60)], fill=skin_color)

    # Hands
    draw.ellipse([center_x - 160, center_y - 150, center_x - 100, center_y - 90], fill=skin_color)
    draw.ellipse([center_x + 100, center_y - 150, center_x + 160, center_y - 90], fill=skin_color)

    # Head
    draw_person_base(draw, center_x, center_y, skin_color, hair_color)
    draw_eyes(draw, center_x, center_y, (100, 60, 30))
    draw_smile(draw, center_x, center_y)

    # Rosy cheeks
    draw.ellipse([center_x - 50, center_y + 5, center_x - 30, center_y + 25],
                 fill=(255, 180, 180))
    draw.ellipse([center_x + 30, center_y + 5, center_x + 50, center_y + 25],
                 fill=(255, 180, 180))

    # Excitement lines around head
    for angle in [30, 60, 120, 150]:
        rad = math.radians(angle)
        x1 = center_x + int(90 * math.cos(rad))
        y1 = center_y - 60 + int(90 * math.sin(rad))
        x2 = center_x + int(120 * math.cos(rad))
        y2 = center_y - 60 + int(120 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 150), width=4)

    # ENFP label
    draw.rectangle([WIDTH//2 - 80, HEIGHT - 120, WIDTH//2 + 80, HEIGHT - 60],
                   fill=(255, 150, 120), outline=(255, 200, 180), width=3)
    draw.text((WIDTH//2 - 40, HEIGHT - 110), "ENFP", fill=(255, 255, 255))

    img.save(os.path.join(OUTPUT_DIR, "mbti_enfp.png"))
    print("Generated mbti_enfp.png")

def generate_entp():
    """ENTP: Dark background + person holding lightbulb (ideas)"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # Dark background with subtle gradient
    create_gradient(draw, WIDTH, HEIGHT, (25, 25, 35), (40, 35, 50))

    # Add some abstract thought bubbles/nodes
    import random
    random.seed(123)
    for _ in range(15):
        cx = random.randint(50, WIDTH - 50)
        cy = random.randint(50, 250)
        r = random.randint(3, 8)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(100, 100, 150))

    # Draw person
    center_x, center_y = WIDTH // 2, 400
    skin_color = (240, 200, 170)
    hair_color = (60, 40, 30)

    # Casual smart outfit
    outfit_color = (60, 60, 80)

    # Body
    draw.polygon([(center_x - 90, center_y + 80),
                  (center_x + 90, center_y + 80),
                  (center_x + 110, center_y + 380),
                  (center_x - 110, center_y + 380)], fill=outfit_color)

    # T-shirt collar detail
    draw.polygon([(center_x - 25, center_y + 80),
                  (center_x + 25, center_y + 80),
                  (center_x + 15, center_y + 130),
                  (center_x - 15, center_y + 130)], fill=(80, 80, 100))

    # Left arm down
    draw.polygon([(center_x - 90, center_y + 80),
                  (center_x - 140, center_y + 280),
                  (center_x - 100, center_y + 290),
                  (center_x - 70, center_y + 120)], fill=outfit_color)

    # Right arm holding up lightbulb
    draw.polygon([(center_x + 90, center_y + 80),
                  (center_x + 180, center_y - 50),
                  (center_x + 140, center_y - 70),
                  (center_x + 70, center_y + 60)], fill=outfit_color)

    # Hand
    draw.ellipse([center_x + 150, center_y - 100, center_x + 200, center_y - 50], fill=skin_color)

    # LIGHTBULB!
    bulb_x, bulb_y = center_x + 175, center_y - 180

    # Lightbulb glow
    for r in range(80, 20, -10):
        alpha = 255 - (r * 2)
        glow_color = (255, 255, min(255, 150 + r))
        draw.ellipse([bulb_x - r, bulb_y - r, bulb_x + r, bulb_y + r], fill=glow_color)

    # Lightbulb shape
    draw.ellipse([bulb_x - 35, bulb_y - 45, bulb_x + 35, bulb_y + 25], fill=(255, 255, 200))
    draw.rectangle([bulb_x - 15, bulb_y + 20, bulb_x + 15, bulb_y + 45], fill=(180, 180, 180))
    draw.line([(bulb_x - 15, bulb_y + 28), (bulb_x + 15, bulb_y + 28)], fill=(150, 150, 150), width=2)
    draw.line([(bulb_x - 15, bulb_y + 36), (bulb_x + 15, bulb_y + 36)], fill=(150, 150, 150), width=2)

    # Rays from lightbulb
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = bulb_x + int(50 * math.cos(rad))
        y1 = bulb_y + int(50 * math.sin(rad))
        x2 = bulb_x + int(70 * math.cos(rad))
        y2 = bulb_y + int(70 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 150), width=3)

    # Head
    draw_person_base(draw, center_x, center_y, skin_color, hair_color)
    draw_eyes(draw, center_x, center_y, (40, 40, 60))

    # Smirk / clever smile
    draw.arc([center_x - 25, center_y + 15, center_x + 25, center_y + 40],
             start=10, end=170, fill=(180, 120, 120), width=3)

    # One raised eyebrow
    draw.line([center_x + 10, center_y - 25, center_x + 35, center_y - 35],
              fill=hair_color, width=4)
    draw.line([center_x - 35, center_y - 25, center_x - 10, center_y - 25],
              fill=hair_color, width=4)

    # ENTP label
    draw.rectangle([WIDTH//2 - 80, HEIGHT - 120, WIDTH//2 + 80, HEIGHT - 60],
                   fill=(50, 50, 70), outline=(100, 100, 150), width=3)
    draw.text((WIDTH//2 - 40, HEIGHT - 110), "ENTP", fill=(200, 200, 255))

    img.save(os.path.join(OUTPUT_DIR, "mbti_entp.png"))
    print("Generated mbti_entp.png")

def generate_infj():
    """INFJ: Purple dreamy background + mysterious person"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # Purple dreamy gradient
    create_gradient(draw, WIDTH, HEIGHT, (80, 40, 120), (40, 20, 80))

    # Add dreamy particles/stars
    import random
    random.seed(789)
    for _ in range(50):
        cx = random.randint(20, WIDTH - 20)
        cy = random.randint(20, HEIGHT - 20)
        r = random.randint(1, 4)
        brightness = random.randint(150, 255)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(brightness, brightness, min(255, brightness + 50)))

    # Mysterious aura/glow around person position
    center_x, center_y = WIDTH // 2, 380
    for r in range(200, 50, -20):
        glow_alpha = 30 + (200 - r)
        draw.ellipse([center_x - r, center_y - r + 50, center_x + r, center_y + r + 50],
                     fill=(100 + r//4, 60, 140 + r//5))

    skin_color = (250, 225, 200)
    hair_color = (30, 20, 40)

    # Flowing robe/cloak
    robe_color = (70, 40, 100)

    # Body with flowing robes
    # Main robe
    draw.polygon([(center_x - 100, center_y + 70),
                  (center_x + 100, center_y + 70),
                  (center_x + 180, center_y + 450),
                  (center_x - 180, center_y + 450)], fill=robe_color)

    # Robe folds
    for i in range(3):
        x_offset = -60 + i * 60
        draw.polygon([(center_x + x_offset, center_y + 100),
                      (center_x + x_offset + 20, center_y + 400),
                      (center_x + x_offset + 40, center_y + 400),
                      (center_x + x_offset + 20, center_y + 100)],
                     fill=(60, 35, 90))

    # Hood effect - partial
    draw.arc([center_x - 100, center_y - 80, center_x + 100, center_y + 100],
             start=200, end=340, fill=(50, 30, 70), width=25)

    # Arms hidden in sleeves (crossed)
    draw.ellipse([center_x - 70, center_y + 150, center_x + 70, center_y + 220],
                 fill=robe_color)

    # Head
    draw_person_base(draw, center_x, center_y, skin_color, hair_color)

    # Mysterious deep eyes
    eye_offset_x = 20
    eye_offset_y = -5
    eye_radius = 10

    # Slightly shadowed eyes
    draw.ellipse([center_x - eye_offset_x - eye_radius, center_y + eye_offset_y - eye_radius,
                  center_x - eye_offset_x + eye_radius, center_y + eye_offset_y + eye_radius],
                 fill=(50, 30, 70))
    draw.ellipse([center_x + eye_offset_x - eye_radius, center_y + eye_offset_y - eye_radius,
                  center_x + eye_offset_x + eye_radius, center_y + eye_offset_y + eye_radius],
                 fill=(50, 30, 70))

    # Small light reflection in eyes
    draw.ellipse([center_x - eye_offset_x - 3, center_y + eye_offset_y - 5,
                  center_x - eye_offset_x + 1, center_y + eye_offset_y - 1],
                 fill=(200, 200, 255))
    draw.ellipse([center_x + eye_offset_x - 3, center_y + eye_offset_y - 5,
                  center_x + eye_offset_x + 1, center_y + eye_offset_y - 1],
                 fill=(200, 200, 255))

    # Gentle mysterious smile
    draw.arc([center_x - 15, center_y + 20, center_x + 15, center_y + 40],
             start=0, end=180, fill=(200, 150, 150), width=2)

    # Third eye symbol on forehead (INFJ intuition)
    draw.ellipse([center_x - 8, center_y - 45, center_x + 8, center_y - 30],
                 fill=(150, 100, 180), outline=(200, 150, 220), width=2)

    # Mystical symbols floating around
    for angle in [45, 135, 225, 315]:
        rad = math.radians(angle)
        sx = center_x + int(150 * math.cos(rad))
        sy = center_y - 50 + int(100 * math.sin(rad))
        # Small diamond shapes
        draw.polygon([(sx, sy - 15), (sx + 10, sy), (sx, sy + 15), (sx - 10, sy)],
                     fill=(180, 150, 220))

    # INFJ label
    draw.rectangle([WIDTH//2 - 80, HEIGHT - 120, WIDTH//2 + 80, HEIGHT - 60],
                   fill=(80, 50, 110), outline=(150, 120, 180), width=3)
    draw.text((WIDTH//2 - 35, HEIGHT - 110), "INFJ", fill=(230, 210, 255))

    img.save(os.path.join(OUTPUT_DIR, "mbti_infj.png"))
    print("Generated mbti_infj.png")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating MBTI character illustrations...")
    generate_intj()
    generate_enfp()
    generate_entp()
    generate_infj()
    print("All images generated successfully!")
