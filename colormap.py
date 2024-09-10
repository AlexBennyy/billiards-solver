from PIL import Image
from collections import Counter

image_path = '/Users/alexbenny/Downloads/poolproject/sample1.png'

# Load the image

def find_prominent_color(image_path):
    # Open the image and convert it to RGB mode
    img = Image.open(image_path).convert("RGB")
    
    # Resize the image to a small size for faster processing
    
    # Get colors from the image
    colors = img.getdata()
    
    # Count the occurrence of each color
    color_count = Counter(colors)
    
    # Find the most common color
    prominent_color = color_count.most_common(1)[0][0]
    
    return prominent_color

def highlight_prominent_color(image_path):
    # Get the most prominent color
    color = find_prominent_color(image_path)
    
    # Create a new image with the most prominent color
    img = Image.new("RGB", (100, 100), color)
    img.show()  # Show the image (can be saved using img.save('output.png'))

# Usage example
highlight_prominent_color(image_path)
