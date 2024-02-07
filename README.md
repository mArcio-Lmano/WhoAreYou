# Who Are You

## Overview

The Celebrities Classifier project is a three-part system designed to scrape images from the web, classify them using a machine learning model, and provide a user-friendly interface for interaction. The project's primary goal is to accurately identify and categorize images of celebrities.

## Project Structure

### 1. Web Scraper

The web scraper component is responsible for collecting images of celebrities from various online sources. It uses web scraping techniques to gather a diverse dataset for training and testing the model.

#### 1. Setup and Usage

To use the web scraper component effectively, you need to provide a User-Agent header for HTTP requests. This helps mimic legitimate browser behavior and avoid being blocked by websites.

#### Creating a User-Agent Header JSON File

Create a JSON file named `headers.json` and specify the User-Agent header value. An example is provided below:

```json
{
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
}
```

#### Obtaining Your User-Agent Header

You can obtain your User-Agent header directly from your browser's developer tools. Here's how:

1. Open your browser and navigate to the webpage you plan to scrape.
2. Right-click anywhere on the page and select "Inspect" or press `Ctrl+Shift+I` (Cmd+Option+I on Mac) to open the developer tools.
3. In the developer tools panel, go to the "Network" tab.
4. Reload the webpage by pressing `Ctrl+R` (Cmd+R on Mac) or clicking the reload button.
5. In the list of network requests, locate the first request (typically the webpage itself) and click on it.
6. In the headers section of the request details, find the "User-Agent" header. This is your User-Agent string.

You can copy your User-Agent string from the developer tools and use it directly when running the web scraper script. There's no need to create a separate `headers.json` file.


```bash
# Install required dependencies
pip3 install -r requirements.txt

# Run the web scraper. 
python3 web_scraper.py <celebrity_name> <num_images> [--verbose]
```
The use of the `--verbose` flag is not recommended except for debugging purposes.

**Check for any errors or exceptions during execution**
### 2. Image Classification Model
<!-- 
The image classification model is the core of the project, responsible for accurately classifying the scraped images. It employs state-of-the-art machine learning techniques, possibly leveraging pre-trained models, to achieve high accuracy in celebrity image classification.

#### Setup and Usage

```bash
# Install required dependencies
pip install -r requirements.txt

# Train the image classification model
python train_model.py

# Evaluate the model's performance
python evaluate_model.py
``` -->

### 3. User Interface

<!-- The user interface provides an intuitive way for users to interact with the Celebrities Classifier. Users can upload images, and the system will predict and display the celebrity present in the image.

#### Setup and Usage

```bash
# Install required dependencies
pip install -r requirements.txt

# Run the user interface
python user_interface.py
``` -->