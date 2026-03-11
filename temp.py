import os
import shutil
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(xml_file, classes):
    """
    Converts a single Pascal VOC XML file to YOLO TXT format.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Get image dimensions
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    yolo_data = []

    for obj in root.iter('object'):
        cls_name = obj.find('name').text
        if cls_name not in classes:
            continue
        
        cls_id = classes.index(cls_name)
        xmlbox = obj.find('bndbox')
        
        # Extract coordinates
        xmin = float(xmlbox.find('xmin').text)
        ymin = float(xmlbox.find('ymin').text)
        xmax = float(xmlbox.find('xmax').text)
        ymax = float(xmlbox.find('ymax').text)

        # Calculate YOLO format: center_x, center_y, width, height (normalized)
        x_center = (xmin + xmax) / 2.0 / w
        y_center = (ymin + ymax) / 2.0 / h
        width = (xmax - xmin) / w
        height = (ymax - ymin) / h

        yolo_data.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    return yolo_data

def convert_xml_label_to_txt(input_xml, output_directory):
    class_list = ["helmet", "head"] 
    
    if os.path.exists(input_xml):
        # 1. Get the base filename (e.g., 'hard_hat_workers0')
        file_base_name = os.path.splitext(os.path.basename(input_xml))[0]
        
        # 2. Combine with directory and new extension
        output_path = os.path.join(output_directory, f"{file_base_name}.txt")
        
        results = convert_voc_to_yolo(input_xml, class_list)
        
        with open(output_path, "w") as f:
            f.write("\n".join(results))
        print(f"Success! Conversion saved to {output_path}")
    else:
        print(f"Error: {input_xml} not found.")
        
def copy_file(source_file,destination_file):
    try:
        # Copy the file, including metadata
        shutil.copy2(source_file, destination_file)
        print(f"File '{source_file}' copied to '{destination_file}' successfully.")
    except shutil.SameFileError:
        print("Source and destination represent the same file.")
    except PermissionError:
        print("Permission denied.")
    except IsADirectoryError:
        print("Destination is a directory (use shutil.copy() if this is intended).")
    except FileNotFoundError:
        print("Source file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


raw_dataset_path_images = "Raw_dataset\images"
raw_dataset_path_labels = "Raw_dataset\labels"

image_data = os.listdir(raw_dataset_path_images)
label_data = os.listdir(raw_dataset_path_labels)

output_images_data_path_train = "dataset/train/images"
output_labels_data_path_train = "dataset/train/labels"

output_images_data_path_val = "dataset/val/images"
output_labels_data_path_val = "dataset/val/labels"



val_percantage = len(image_data)*0.8

# copy_file("Raw_dataset\images\hard_hat_workers0.png",output_images_data_path_train)
    
for idx,img,xml in zip(range(len(image_data)),image_data,label_data):
    img_path = os.path.join(raw_dataset_path_images,img)
    xml_path = os.path.join(raw_dataset_path_labels,xml)
    if (idx <= val_percantage):
        copy_file(img_path,output_images_data_path_train)
        convert_xml_label_to_txt(xml_path,output_labels_data_path_train)
    else:
        copy_file(img_path,output_images_data_path_val)
        convert_xml_label_to_txt(xml_path,output_labels_data_path_val)
        