from bs4 import BeautifulSoup
from time import sleep
import requests
import os
import sys


# User Variables: Celebrity and number of images the user wants
CELEB = sys.argv[1]  # Celebrity name provided as the first command-line argument
NUM_IMGS = int(sys.argv[2])  # Number of images provided as the second command-line argument

# URL for the site used to get the images
IMAGES_URL = f"https://www.gettyimages.pt/fotos/42?family=editorial&assettype=image&phrase={CELEB}&sort=mostpopular&page="
IMG_PATH = "img"  # Directory to save the downloaded images


def getImages(celeb, n_images):
    """
    Download images of a given celebrity from a website.
    
    Args:
    - celeb: The name of the celebrity.
    - n_images: The number of images to download.
    """
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"}
    page_number = 1
    counter = 0
    
    while counter < n_images:
        response = requests.get(IMAGES_URL + str(page_number), headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all("img")
        
        for img_tag in img_tags:
            if counter >= n_images:
                return counter # Break the function if the desired number of images is reached
            try: 
                img_url = img_tag.get('src')
                img_name = os.path.join(IMG_PATH, f"{celeb}_{counter}.jpg")
                with open(img_name, 'wb') as img_file:
                    img_file.write(requests.get(img_url).content)
                counter += 1
                
            except Exception as e:
                print(f"Failed to download image: {e}")
        
        page_number += 1
        
    return counter

def main():
    # Create the image directory if it does not exist
    if not os.path.exists(IMG_PATH):
        os.makedirs(IMG_PATH)
    
    c = getImages(celeb=CELEB, n_images=NUM_IMGS)    
    
    print(f"Downloaded {c} images of {CELEB}.")
    
if __name__ == "__main__":
    main()
