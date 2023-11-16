"""
Creates n*n sub-images in a grid like manner
"""

from PIL import Image
import os

def extract_subimages(input_image_path, output_folder, n):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the input image
    with Image.open(input_image_path) as img:
        # Get the dimensions of the input image
        width, height = img.size

        # Calculate the number of sub-images in each dimension
        num_subimages_x = width // n
        num_subimages_y = height // n

        # Extract and save sub-images
        for i in range(num_subimages_x):
            for j in range(num_subimages_y):
                left = i * n
                upper = j * n
                right = left + n
                lower = upper + n

                # Crop and save the sub-image
                subimage = img.crop((left, upper, right, lower))
                subimage_name = f"subimage_{i}_{j}.png"
                subimage_path = os.path.join(output_folder, subimage_name)
                subimage.save(subimage_path)

if __name__ == "__main__":
    # Input image path
    input_image_path = "plant3.jpg"

    # Output folder for sub-images
    output_folder = "subImages/"

    # Size of each sub-image (n x n pixels)
    n = 60

    extract_subimages(input_image_path, output_folder, n)
