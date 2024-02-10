import os
import sys
import cv2

def process_images(celeb_dir, log=False):
    log_path = "log.txt"
    if not os.path.exists(celeb_dir):
        print(f"Directory does not exist.: {celeb_dir}")
        sys.exit(1)
        
    if log:
        if not os.path.exists(log_path): # Check if log file is not the directory
            print("Log file not found. Try executing without the log flag.")
            sys.exit(1)
            
        with open(log_path, "r") as log_file: # Open Log file
            img_path = log_file.read()

        if os.path.basename(img_path) not in sorted(os.listdir(celeb_dir)): # Check if we are loking in the rigth directory
            print(f"Image {img_path} not found in directory. Checking Next")
            return 1
        
        img_index = sorted(os.listdir(celeb_dir)).index(os.path.basename(img_path)) # Retrive last saw image
        imgs = sorted(os.listdir(celeb_dir))[img_index + 1:] # Retrive the images that were not saw
            
    else: # If no log file was used retrive all images
        imgs = sorted(os.listdir(celeb_dir))
    
    for f in imgs: # Iterate over the images
        img_path = os.path.join(celeb_dir, f)
        img = cv2.imread(img_path) 
        
        cv2.imshow(img_path, img)
        print(2*"\t"+img_path) #### Debug (REMOVE) ####
            
        key = cv2.waitKey(0)  # Wait for a key press
        cv2.destroyAllWindows() # Close all images
            
        if key == ord("x"): # "x" to delete
            os.remove(img_path) # Delete image
        elif key == ord("q"):  # "q" key to quit
            with open(log_path, "w") as log_file:
                log_file.write(img_path) # Save the last image seen in a log file for later use
            sys.exit(0)
    
    return 0

        
def rename_images(celeb_dir):
    celeb = os.path.basename(celeb_dir)
    print(celeb)
    return 1
    
def main():
    status = 1
    log = "--log" in sys.argv # Check for "--log" flag
    print(log) #### Debug (REMOVE) ####
    path = "img"
    if not os.path.exists(path): # Check if there is an "img" folder
        print(f"Folder {path} not found")
        sys.exit(1)

    files = [f for f in os.listdir(path)]
    if files:
        print(f"Celebrities found: {len(files)}")
        for img_name in files:
            print(f"\t{img_name}")
            file_name = os.path.join(path, img_name)
            status = process_images(file_name, log)
            
        if not status:
            status = rename_images(os.path.join(path, file_name))
    else:
        print(f"No celebrities found in the folder {path}.")
        sys.exit(1)
    return status
        
if __name__ == "__main__":
    status = main()
    if not status:
        print("Script executed with no errors")
    else:
        print(f"Status Error {status}")
        
    