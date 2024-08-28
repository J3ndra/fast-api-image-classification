import os
from PIL import Image

# Input and output directories
input_dir = 'datasets/images/'
output_dir = 'datasets/preprocessed/'
image_size = (128, 128)  # Resize images to 128x128 pixels

def preprocess_image(image_path, output_path):
    """Resize the image and save it to the output path."""
    try:
        img = Image.open(image_path)
        img = img.resize(image_size)
        img.save(output_path)
        print(f"Processed {output_path}")
    except Exception as e:
        print(f"Failed to process {image_path}: {e}")

def preprocess_images(input_dir, output_dir):
    """Preprocess all images from input_dir, preserving subdirectory structure."""
    for root, _, files in os.walk(input_dir):
        # Calculate the relative path to preserve subdirectory structure
        relative_path = os.path.relpath(root, input_dir)
        # Create the corresponding directory in the output path
        output_subdir = os.path.join(output_dir, relative_path)
        
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)
        
        for img_name in files:
            input_path = os.path.join(root, img_name)
            output_path = os.path.join(output_subdir, img_name)
            
            # Process only files that are images
            if img_name.endswith((".jpg", ".png", ".jpeg", ".bmp")):
                preprocess_image(input_path, output_path)

if __name__ == "__main__":
    preprocess_images(input_dir, output_dir)
