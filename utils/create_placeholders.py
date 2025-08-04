#!/usr/bin/env python3
"""
Create placeholder images for the blog articles
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_placeholder_image(filename, title, color=(70, 130, 180), size=(1200, 600)):
    """Create a placeholder image with title text"""
    # Create image
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
        small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 48)
            small_font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), title, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 - 20
    
    # Draw title
    draw.text((x, y), title, fill='white', font=font)
    
    # Draw subtitle
    subtitle = "Daudi's Perspective"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=small_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (size[0] - subtitle_width) // 2
    subtitle_y = y + text_height + 10
    
    draw.text((subtitle_x, subtitle_y), subtitle, fill='lightgray', font=small_font)
    
    return img

def main():
    """Create all placeholder images"""
    # Ensure static/images directory exists
    os.makedirs('static/images', exist_ok=True)
    
    # Define images to create
    images = [
        ('network-africa.jpg', 'African Networks', (34, 139, 34)),  # Forest Green
        ('land-cruiser.jpg', 'Land Cruiser', (139, 69, 19)),        # Saddle Brown
        ('turbofan-engine.jpg', 'Turbofan Engine', (70, 130, 180)), # Steel Blue
        ('ubuntu-terminal.jpg', 'Ubuntu Terminal', (233, 84, 32)),   # Ubuntu Orange
        ('python-microcontroller.jpg', 'Python & MCU', (55, 118, 171)), # Python Blue
        ('embedded-systems.jpg', 'Embedded Systems', (128, 128, 128))    # Gray
    ]
    
    for filename, title, color in images:
        img = create_placeholder_image(filename, title, color)
        img.save(f'static/images/{filename}', 'JPEG', quality=85)
        print(f"Created {filename}")
    
    print("All placeholder images created successfully!")
    print("\nTo replace with real images:")
    print("1. Download appropriate images from Unsplash or other free sources")
    print("2. Resize them to 1200x600 pixels")
    print("3. Replace the files in static/images/")

if __name__ == "__main__":
    main()