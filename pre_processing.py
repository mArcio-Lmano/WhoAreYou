import os
import sys
import cv2
import shutil
import imutils 
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator

from time import sleep


# Set the WINEPREFIX environment variable
os.environ["WINEPREFIX"] = "/home/talocha/.wine"

def processImages(celeb_dir, log=False):
    """
    Process images in a specified directory, optionally continuing from the last viewed image.

    This function processes images located in the 'celeb_dir' directory. If the 'log' flag is set to True, 
    it checks for a log file containing the path of the last viewed image. If found, it continues processing 
    images from the next one. If the 'log' flag is False or if the log file is not found, it processes all images 
    in the directory.

    Args:
        celeb_dir (str): The directory path where the images are located.
        log (bool, optional): A flag indicating whether to continue processing from the last viewed image 
                             (default is False).

    Returns:
        tuple: A tuple containing an exit status code (0 for success, 1 for failure) and the updated log status.

    Raises:
        FileNotFoundError: If the specified directory 'celeb_dir' does not exist.
        IndexError: If the last viewed image in the log file is not found in the directory.
    """
    log_path = "log.txt"
    
    # Check if the directory 'celeb_dir' exists
    if not os.path.exists(celeb_dir):
        raise FileNotFoundError(f"Directory '{celeb_dir}' does not exist.")
        
    if log:
        # Check if log file exists
        if not os.path.exists(log_path):
            raise FileNotFoundError(f"Log file not found {log_path}. Try executing without the log flag.")
            
        with open(log_path, "r") as log_file: # Open Log file
            img_path = log_file.read()

        # Check if the last viewed image exists in the directory
        if os.path.basename(img_path) not in sorted(os.listdir(celeb_dir)):
            print(f"Image {img_path} from log file not found in directory. Checking Next")
            return 1, log
        
        # Retrieve the index of the last viewed image and get the subsequent images
        img_index = sorted(os.listdir(celeb_dir)).index(os.path.basename(img_path))
        imgs = sorted(os.listdir(celeb_dir))[img_index + 1:]
        log = False
            
    else: # If no log file was used, retrieve all images
        imgs = sorted(os.listdir(celeb_dir))
    
    # Process images using the delete_imgs function
    deleteImgs(imgs=imgs, celeb_dir=celeb_dir, log_path=log_path)
    # sleep(20)
    return 0, log


def deleteImgs(imgs, celeb_dir, log_path):
    """
    Display images from a specified directory and allow the user to decide whether to delete them.

    This function iterates through a list of image filenames provided in the 'imgs' parameter, 
    displays each image using OpenCV, and waits for user input to determine whether to delete 
    the image or proceed to the next one. The user can press 'x' to delete the image or 'q' to 
    quit the process. If the user quits, the function saves the path of the last viewed image 
    into a log file specified by 'log_path'.

    Args:
        imgs (list): A list of image filenames to be processed.
        celeb_dir (str): The directory path where the images are located.
        log_path (str): The file path for storing the log of the last viewed image.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified directory 'celeb_dir' does not exist.
        ValueError: If 'imgs' is not a list or if any of the elements in 'imgs' is not a valid image filename.
    """
    # Check if the directory 'celeb_dir' exists
    if not os.path.exists(celeb_dir):
        raise FileNotFoundError(f"Directory '{celeb_dir}' does not exist.")
    
    # Iterate over the images
    for f in imgs: 
        # Construct the full path to the image file
        img_path = os.path.join(celeb_dir, f)
        
        # Read the image using OpenCV
        img = cv2.imread(img_path) 
        
        # Display the image
        cv2.imshow(img_path, img)
        print(2 * "\t" + img_path)  # Debug
        
        # Wait for a key press
        key = cv2.waitKey(0)
        
        # Close all displayed images
        cv2.destroyAllWindows() 
        
        # If the user pressed "x", delete the image
        if key == ord("x"): 
            os.remove(img_path) 
        # If the user pressed "q", save the path of the last viewed image into a log file and exit
        elif key == ord("q"):  
            with open(log_path, "w") as log_file:
                log_file.write(img_path)
            sys.exit(0)
        # If any other key is pressed, proceed to the next image
    

def renameImages(celeb_dir):
    """
    Rename all images in the specified directory with a counter appended to the filename.

    Args:
        celeb_dir (str): The directory path containing the images to be renamed.

    Returns:
        int: Status code indicating success (0).
    """
    # Get a sorted list of files in the directory
    files = sorted(os.listdir(celeb_dir))
    
    # Initialize a counter
    counter = 0
    
    # Extract the basename of the directory as the celebrity name
    celeb = os.path.basename(celeb_dir)
    
    # Iterate over each file in the directory
    for file in files:
        # Construct the old and new file paths
        old_name = os.path.join(celeb_dir, file)
        new_file_name = celeb + f"_{counter}.jpg"
        new_name = os.path.join(celeb_dir, new_file_name)
        
        # Increment the counter
        counter += 1
        
        # Rename the file
        os.rename(old_name, new_name)
    
    # Return success status code
    return 0


def resizeNormalizeAugment(celeb_dir, verbose):
    """
    Resize images in the specified directory to 224x224 pixels and normalize pixel values to the range [0, 1].

    Args:
        celeb_dir (str): Path to the directory containing images.

    Returns:
        None
    """
    # List all files in the directory
    files = os.listdir(celeb_dir)

    # Process each image file
    for file in files:
        # Construct the full file path
        file_path = os.path.join(celeb_dir, file)
        
        # Read the image using OpenCV
        img = cv2.imread(file_path)
        
        # Resize the image to 224x224 pixels
        img_resized = cv2.resize(src=img, dsize=[224, 224])
        
        # Normalize pixel values to the range [0, 1]
        img_normalized = cv2.normalize(img_resized, None, 0, 1.0, cv2.NORM_MINMAX)
        
        # Apply data augmentation
        imgs_augmented = dataAugment(img_normalized)
        
        # Save the normalized image
        original_path = os.path.join(celeb_dir, file)
        cv2.imwrite(original_path, img_normalized)
        
        # Save augmented images with appropriate file names
        file_identifier = file.split(".")[0]
        partial_path = os.path.join(celeb_dir, file_identifier)
        
            # Cycle through all the augmented images and create the respective files
        for i, image in enumerate(imgs_augmented):
            path = partial_path + f"_{i}.jpg"
            cv2.imwrite(path, image)
            

def dataAugment(image):
    """
    Apply data augmentation to an image by rotating it at angles of 90, 180, and 270 degrees.

    Args:
        image (numpy.ndarray): Input image to be augmented.

    Returns:
        list: A list containing the rotated images.
    """
    # Define rotation angles
    angles = [90, 180, 270]
    
    # Initialize list to store rotated images
    rotated_images = []
    
    # Rotate the image at each angle and append to the list
    for angle in angles:
        rotated_image = imutils.rotate(image, angle)
        rotated_images.append(rotated_image)
    
    # Return the list of rotated images
    return rotated_images


def main():
    """
    Main function to orchestrate image processing tasks.

    Returns:
        int: Status code indicating the success or failure of the script.
             0: Script executed successfully.
             1: Image path from log file not found in any directory. Check log file.
             Other: Error occurred during script execution.
    """
    # Initialize status and flags based on command-line arguments
    status = 1
    log = "--log" in sys.argv  # Check for "--log" flag
    verbose = "--verbose" in sys.argv  # Check for "--verbose" flag
    bak = "--bak" in sys.argv
    
    # Flags used
    print(f"Log: {log}")
    print(f"Verbose: {verbose}")
    print(f"BAK: {bak}")

    # Set up path for image processing
    path = "img"

    # Create a backup folder if requested
    if bak:
        shutil.copytree(path, path + "_BAK", copy_function=shutil.copy)

    # Check if the "img" folder exists
    if not os.path.exists(path):
        print(f"Folder {path} not found")
        sys.exit(1)

    # Get a list of image files in the folder
    files = [f for f in os.listdir(path)]

    if files:
        # Print the number of celebrities found and process each image
        print(f"Celebrities found: {len(files)}")
        for img_name in files:
            print(f"\t{img_name}")
            file_name = os.path.join(path, img_name)
            # Process the image
            status, log = processImages(file_name, log)
            if not status:
                status = renameImages(file_name)
                resizeNormalizeAugment(file_name, verbose)
                renameImages(file_name)
    else:
        # Handle case when no celebrities are found
        print(f"No celebrities found in the folder {path}.")
        sys.exit(1)

    # Clean up backup folder if not used and successful
    if not status and bak:
        while True:
            remove_bak = input("Do you want to remove the backup folder? [Y/n]: ").strip().lower()
            if remove_bak in ["y", "yes"]:
                shutil.rmtree(path + "_BAK")
                print("Backup folder deleted successfully.")
                break
            elif remove_bak in ["n", "no"]:
                print(f"Backup folder saved as: {path}_BAK")
                break
            else:
                print("Invalid input. Please enter 'Y' or 'N' to confirm your choice.")

    return status
        
if __name__ == "__main__":
    status = main()
    if not status:
        print("Script executed with no errors")
    elif status == 1:
        raise IndexError(f"Image path from log file not found in any directory. Check log file")
    else:
        print(f"Exit code {status}")
        
    