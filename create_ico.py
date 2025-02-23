from PIL import Image
import os

def create_ico():
    # Standard Windows icon sizes
    sizes = [16, 24, 32, 48, 64, 128, 256]
    
    # Load the highest resolution image as our source
    img = Image.open('assets/icons.iconset/icon_512x512@2x.png')
    
    # Create a list to store our images
    imgs = []
    
    # Process each size
    for size in sizes:
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        if resized_img.mode != 'RGBA':
            resized_img = resized_img.convert('RGBA')
        imgs.append(resized_img)
    
    # Save as ICO with all sizes
    # Windows typically uses 32x32 as the default
    idx_32 = sizes.index(32)
    imgs.insert(0, imgs.pop(idx_32))
    
    # Save with all sizes included
    imgs[0].save('assets/AppIcon.ico', 
                format='ICO',
                sizes=[(size, size) for size in sizes])

if __name__ == '__main__':
    create_ico() 