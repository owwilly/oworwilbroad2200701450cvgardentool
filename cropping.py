import cv2
import numpy as np
import os
import xml.etree.ElementTree as ET

# Specify the parent directory that contains the images and labels subfolders
parent_dir = 'crops_data'

# Iterate over the images in the images subfolder
images_dir = os.path.join(parent_dir, 'images')

for filename in os.listdir(images_dir):
    if filename.endswith('.jpg'):
        image_path = os.path.join(images_dir, filename)

        # Read the image
        image = cv2.imread(image_path)

        # Parse the corresponding XML file from the labels subfolder
        labels_dir = os.path.join(parent_dir, 'labels')
        xml_path = os.path.join(labels_dir, filename.replace('.jpg', '.xml'))

        # Parse the XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Extract the class label and bounding box coordinates
        for obj in root.findall('object'):
            class_label = obj.find('name').text
            xmin = int(obj.find('bndbox/xmin').text)
            ymin = int(obj.find('bndbox/ymin').text)
            xmax = int(obj.find('bndbox/xmax').text)
            ymax = int(obj.find('bndbox/ymax').text)

            # Check if the bounding box coordinates are within the image boundaries
            if xmin < xmax and ymin < ymax and xmax <= image.shape[1] and ymax <= image.shape[0]:
                # Crop the image based on the bounding box coordinates
                cropped_image = image[ymin:ymax, xmin:xmax]

                # Create a folder for the class label if it doesn't exist
                class_folder = os.path.join(parent_dir, class_label)
                if not os.path.exists(class_folder):
                    os.makedirs(class_folder)

                # Save the cropped image in the class folder
                save_path = os.path.join(class_folder, f'{filename.replace(".jpg", "")}_{xmin}_{ymin}_{xmax}_{ymax}.jpg')
                cv2.imwrite(save_path, cropped_image)

                