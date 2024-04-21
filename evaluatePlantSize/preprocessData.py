from PIL import Image, ImageOps

"""
Function for processing one image-label pair
"""

BROWN = (49, 42, 31)


def pad(image_path, label_path, image_output_folder, label_output_folder, desired_size_data = 572, desired_size_label = 388):
    """
    Pads image and label, so their dimensions match the desired size
    I am not sure if this is how images should be pre-processed for the U-Net architecture
    """
    image = Image.open(image_path)
    label = Image.open(label_path)

    # Transform the label to black and white
    def check_if_black(pixel):
        return pixel if pixel == (0, 0, 0) else (255, 255, 255)

    if label.mode != 'RGB':
        label = label.convert('RGB')
    new_data = [check_if_black(pixel) for pixel in label.getdata()]
    label.putdata(new_data)

    width, height = image.size
    #print(image.size, label.size)

    padding_top = max(0, (width-height)//2)
    padding_bottom = max(0, width-height-padding_top)
    padding_left = max(0, (height-width)//2)
    padding_right = max(0, height-width-padding_left)

    image_size = max(width, height)
    if image_size > desired_size_label:
        pass  # this should be handlend properly, should no be problem for now
    # pad the label
    padding_label = (desired_size_label - image_size)//2
    # pad the image
    padding_image = (desired_size_data - image_size)//2

    padded_image = ImageOps.expand(image, border=(padding_left+padding_image, padding_top+padding_image, padding_right+padding_image, padding_bottom+padding_image), fill=BROWN)
    padded_label = ImageOps.expand(label, border=(padding_left+padding_label, padding_top+padding_label, padding_right+padding_label, padding_bottom+padding_label), fill="black")

    padded_image.save(image_output_folder + image_path.split("/")[-1])
    padded_label.save(label_output_folder + label_path.split("/")[-1])

# Example usage
path_image = 'project/pictures/datapoints/ara2013_plant001_rgb.png'
path_label = 'project/pictures/labels/ara2013_plant001_label.png'
label_output = "project/pictures/processed/labels/"
image_output = "project/pictures/processed/images/"
pad(path_image, path_label, image_output, label_output)




