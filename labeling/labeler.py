"""
Program used for giving labels to pictures. The pictures
to be labeled need to be in the same folder
"""

import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv


class ImageLabelingApp:
    def __init__(self, root, image_folder):
        self.root = root
        self.root.title("Image Labeling Tool")

        self.image_folder = image_folder
        self.image_list = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        self.current_index = 0

        self.label_var = tk.DoubleVar()
        self.label_var.set(0.5)  # Default label value

        self.create_widgets()
        self.load_image()

        self.bind_arrow_keys()

        self.generated_data = [["R", "G", "B", "Label"]]
        self.current_image_colors = [0, 0, 0]

    def create_widgets(self):
        self.label_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, label="Label", variable=self.label_var)
        self.label_slider.pack(pady=10)

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.save_button = tk.Button(self.root, text="Save", command=self.save_label)
        self.save_button.pack(pady=5)

    def load_image(self):
        if self.current_index < len(self.image_list):
            image_path = os.path.join(self.image_folder, self.image_list[self.current_index])
            image = Image.open(image_path)

            tot = [0, 0, 0]
            for i in range(10):
                for j in range(10):
                    p = image.getpixel((i, j))
                    # I did this on purpose
                    tot[0] += p[2]
                    tot[1] += p[1]
                    tot[2] += p[1]
            self.current_image_colors = [tot[0]/100, tot[1]/100, tot[2]/100]

            image = image.resize((400, 400))  # Adjust the size as needed
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo
        else:
            self.image_label.config(text="No more images to label")

    def bind_arrow_keys(self):
        self.root.bind("<Left>", lambda event: self.adjust_slider(-0.01))
        self.root.bind("<Right>", lambda event: self.adjust_slider(0.01))
        self.root.bind("<Down>", lambda event: self.adjust_slider(-0.05))
        self.root.bind("<Up>", lambda event: self.adjust_slider(0.05))
        self.root.bind("<Return>", lambda event: self.next_image())
        self.root.bind("0", lambda event: self.zero())

    def adjust_slider(self, step):
        current_value = self.label_var.get()
        new_value = max(0, min(1, current_value + step))
        self.label_var.set(new_value)

    def zero(self):
        self.label_var.set(0.0)
        self.next_image()

    def next_image(self):
        self.generated_data.append(self.current_image_colors + [self.label_var.get()])
        self.current_index += 1
        self.label_var.set(0.5)  # Reset slider value to the default
        self.load_image()

    def save_label(self):
        self.generated_data.pop(1) # first datapoint is faulty
        with open("labeledData.txt", mode='w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)
            # Write the data to the CSV file
            writer.writerows(self.generated_data)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    image_folder = filedialog.askdirectory(title="Select Image Folder")
    if image_folder:
        app = ImageLabelingApp(root, image_folder)
        root.mainloop()
