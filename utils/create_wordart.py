#!/usr/bin/env python3
"""
Generates stylish and artistic header images for the blog articles
using procedural generation techniques with Pillow. This version includes
robust error handling and safer coordinate generation.
"""

import os
import json
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

def find_font(preferred_fonts, default_size=72):
    """
    Finds an available TrueType font from a list of common system paths.
    This makes the script more portable across different operating systems.
    """
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:\\Windows\\Fonts\\Verdana.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]
    for font_name in preferred_fonts:
        try:
            return ImageFont.truetype(font_name, default_size)
        except IOError:
            continue
    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, default_size)
        except IOError:
            continue
    return ImageFont.load_default()

def draw_multiline_text(draw, text, xy, font, fill):
    """
    Draws text that automatically wraps and is centered.
    """
    wrapped_lines = textwrap.wrap(text, width=30, break_long_words=False)
    
    line_metrics = []
    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        line_metrics.append({'width': width, 'height': height, 'text': line})

    total_height = sum(m['height'] for m in line_metrics) + (len(line_metrics) - 1) * 10
    
    x, y = xy
    current_y = y - total_height / 2

    for metrics in line_metrics:
        line_x = x - metrics['width'] / 2
        draw.text((line_x + 3, current_y + 3), metrics['text'], font=font, fill=(0, 0, 0, 80))
        draw.text((line_x, current_y), metrics['text'], font=font, fill=fill)
        current_y += metrics['height'] + 10

def generate_artistic_background(draw, size, palette, theme):
    """
    Generates the busy, artistic background with thematic elements and robust error handling.
    """
    width, height = size
    
    for _ in range(250):
        try:
            shape_type = random.choice(['line', 'ellipse', 'rectangle'])
            color = random.choice(palette)
            alpha = random.randint(20, 60)
            fill = (*color, alpha)
            
            # **REVISED & SAFER COORDINATE GENERATION**
            # This method ensures that the bounding box is always valid.
            x1 = random.randint(-50, width + 50)
            y1 = random.randint(-50, height + 50)
            # By adding a positive random number, we guarantee x2 > x1 and y2 > y1
            x2 = x1 + random.randint(10, 200)
            y2 = y1 + random.randint(10, 200)
            box = (x1, y1, x2, y2)

            if shape_type == 'line':
                # Lines don't need a bounding box, so original randomness is fine.
                lx1, ly1 = random.randint(-50, width+50), random.randint(-50, height+50)
                lx2, ly2 = lx1 + random.randint(-200, 200), ly1 + random.randint(-200, 200)
                draw.line([(lx1, ly1), (lx2, ly2)], fill=fill, width=random.randint(1, 4))
            elif shape_type == 'ellipse':
                draw.ellipse(box, fill=fill)
            elif shape_type == 'rectangle':
                draw.rectangle(box, fill=fill)
        except ValueError as e:
            # This safety net will catch any unexpected errors and allow the script to finish.
            print(f"Warning: Skipped drawing a shape due to a Pillow error: {e}")
            continue

    # Thematic elements remain the same
    if theme == 'Networks':
        for _ in range(50):
            start_point = (random.randint(0, width), random.randint(0, height))
            end_point = (random.randint(0, width), random.randint(0, height))
            draw.line([start_point, end_point], fill=(*random.choice(palette), 40), width=1)
    elif theme == 'Linux':
        for _ in range(200):
            x, y = random.randint(0, width), random.randint(0, height)
            draw.rectangle([(x,y), (x+10, y+10)], fill=(*random.choice(palette), 30), width=1)
    # ... other themes ...

def create_generative_art_image(title, subtitle, category, color_start, color_end, size=(1200, 600)):
    """
    Creates a complete generative art image with background and text.
    """
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img, 'RGBA')

    # --- Create the Gradient Background ---
    for y in range(size[1]):
        ratio = y / (size[1] - 1)
        r = int(color_start[0] * (1 - ratio) + color_end[0] * ratio)
        g = int(color_start[1] * (1 - ratio) + color_end[1] * ratio)
        b = int(color_start[2] * (1 - ratio) + color_end[2] * ratio)
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))

    # --- Generate Artistic Overlay ---
    palette = [(int(color_start[0] * (1-r) + color_end[0] * r), int(color_start[1] * (1-r) + color_end[1] * r), int(color_start[2] * (1-r) + color_end[2] * r)) for r in [0, 0.25, 0.5, 0.75, 1.0]]
    generate_artistic_background(draw, size, palette, category)

    # --- Draw Text Plaque for Readability ---
    center_x, center_y = size[0] // 2, size[1] // 2
    plaque_width, plaque_height = 900, 350
    plaque_x1, plaque_y1 = center_x - plaque_width // 2, center_y - plaque_height // 2
    draw.rectangle((plaque_x1, plaque_y1, plaque_x1 + plaque_width, plaque_y1 + plaque_height), fill=(0, 0, 0, 90))

    # --- Load Fonts and Draw Text ---
    title_font = find_font(["Georgia-Bold", "DejaVuSans-Bold", "Verdana-Bold"], 70)
    subtitle_font = find_font(["Verdana", "DejaVuSans"], 32)
    
    draw_multiline_text(draw, title, (center_x, center_y - 20), title_font, fill=(255, 255, 255))
    
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_x = center_x - (subtitle_bbox[2] - subtitle_bbox[0]) / 2
    subtitle_y = center_y + 80
    draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=(230, 230, 230, 200))

    return img.convert('RGB')

def main():
    """
    Main function to generate and save all word art images.
    """
    output_dir = 'static/images'
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open('data/articles.json', 'r') as f:
            articles = json.load(f)['articles']
    except FileNotFoundError:
        print("Error: 'data/articles.json' not found. Cannot generate images.")
        return

    color_palette = {
        'Networks':   ((20, 80, 120), (40, 120, 180)),
        'Automotive': ((100, 80, 60), (140, 110, 90)),
        'Aviation':   ((60, 70, 80), (110, 120, 130)),
        'Linux':      ((200, 80, 40), (230, 120, 60)),
        'Python':     ((50, 100, 150), (80, 130, 190)),
        'Embedded':   ((70, 70, 70), (110, 110, 110)),
        'default':    ((80, 80, 80), (120, 120, 120))
    }

    print("🎨 Generating new artistic images with robust error handling...")
    for article in articles:
        filename = article.get('image', f"{article['id']}.jpg")
        title = article.get('title', 'Untitled')
        category = article.get('category', 'General')
        
        colors = color_palette.get(category, color_palette['default'])
        
        img = create_generative_art_image(
            title=title,
            subtitle=category,
            category=category,
            color_start=colors[0],
            color_end=colors[1]
        )
        
        save_path = os.path.join(output_dir, filename)
        img.save(save_path, 'JPEG', quality=90)
        print(f"✅ Created '{save_path}' for article '{title}'")
    
    print("\n✨ All artistic images generated successfully!")

if __name__ == "__main__":
    main()
