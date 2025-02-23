from PIL import Image
import os

def create_ico():
    # Define the sizes we want in our ico file
    sizes = [16, 32, 48, 64, 128, 256]
    
    # Load the largest image as our source
    img = Image.open('assets/icons.iconset/icon_512x512@2x.png')
    
    # Create a list to store our images
    imgs = []
    
    # Resize the image to all the sizes we need
    for size in sizes:
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        imgs.append(resized_img)
    
    # Save all sizes to a single .ico file
    # The first image in the list will be the default size
    imgs[0].save('assets/AppIcon.ico', format='ICO', sizes=[(img.width, img.height) for img in imgs], append_images=imgs[1:])

if __name__ == '__main__':
    create_ico() 