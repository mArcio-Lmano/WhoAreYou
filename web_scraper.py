from bs4 import BeautifulSoup
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import requests
import os
import sys
import json

def count_faces_from_bytes(image_bytes):
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    # Return the number of detected faces
    return len(faces), faces, image

def getImages(celeb, n_images, verbose, img_path):
    """
    Download images of a given celebrity from a website.
    
    Args:
    - celeb: The name of the celebrity.
    - n_images: The number of images to download.
    """
    with open("headers.json", "r") as f:
        headers = json.load(f)
    imgs_url = f"https://www.gettyimages.pt/fotos/42?family=editorial&assettype=image&phrase={celeb}&sort=mostpopular&page="
    page_number = 1
    counter = 0
    
    while counter < n_images:
        response = requests.get(imgs_url + str(page_number), headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all("img")
        
        for img_tag in img_tags:
            if counter >= n_images:
                return counter # Break the function if the desired number of images is reached
            try: 
                        
                img_url = img_tag.get('src')
                img_bits = requests.get(img_url).content
                
                count_faces_falg, faces, image = count_faces_from_bytes(img_bits)
                img_name = os.path.join(img_path, f"{celeb}_{counter}.jpg")
                
                if count_faces_falg == 1:
                    print("Keeping image")
                    with open(img_name, 'wb') as img_file:
                        img_file.write(img_bits)
                    counter += 1
                else:
                    print(f"Removing image, Found {count_faces_falg} faces")
                    if verbose:
                        for (x, y, w, h) in faces:
                            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        
                        # Display the image with rectangles
                        cv2.imshow('Faces Detected', image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()


            except Exception as e:
                print(f"Failed to download image: {e}")
        
        page_number += 1
        
    return counter

def main():
    if len(sys.argv) < 3: # Make sure that the user introduced the right amountof parameters
        print("Usage: python script.py <celebrity_name> <num_images> [--verbose]")
        sys.exit(1)
    
    # User Variables: Celebrity and number of images the user wants
    celebrity_name = sys.argv[1]  # Celebrity name provided as the first command-line argument
    num_imgs = int(sys.argv[2])  # Number of images provided as the second command-line argument
    verbose = "--verbose" in sys.argv
    
    # URL for the site used to get the images
    img_path = "img"  # Directory to save the downloaded images

    # Create the image directory if it does not exist
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    
    c = getImages(celeb=celebrity_name, n_images=num_imgs, verbose=verbose, img_path=img_path)    
    
    print(f"Downloaded {c} images of {celebrity_name}.")
    
if __name__ == "__main__":
    main()
