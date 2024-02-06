from bs4 import BeautifulSoup
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import requests
import os
import sys
import io






def getImages(celeb, n_images, verbose, img_path):
    """
    Download images of a given celebrity from a website.
    
    Args:
    - celeb: The name of the celebrity.
    - n_images: The number of images to download.
    """
    imgs_url = f"https://www.gettyimages.pt/fotos/42?family=editorial&assettype=image&phrase={celeb}&sort=mostpopular&page="
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"}
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
                
                img_name = os.path.join(img_path, f"{celeb}_{counter}.jpg")
                img_bits = requests.get(img_url).content
                if verbose:
                    img_pixels = io.BytesIO(img_bits)
                    image = Image.open(img_pixels)
                    plt.imshow(image)
                    plt.axis('off')  
                    plt.show()
                with open(img_name, 'wb') as img_file:
                    img_file.write(img_bits)
                counter += 1
                
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
