# Airbnb Full Price Scrap Project

## Motivation and Main Goal:
Getting the final price for each Airbnb property is tedious as it requires to enter each url and look for the final detail

The script allows a user to enter the destination and other search parameters and returns an excel with a complete list
with final prices.

## Installation
Clone the repo and install all dependencies.
Always recommended to create a virtual environment first.
`pip install -r requirements.txt`

We also need to install Chrome and chromedriver. Make sure you have same versions.
https://chromedriver.chromium.org/downloads

In the terminal run `main.py` to get prompted for searching parameters.
After some time, an `xlsx` file will be saved with the results.

### To-Do:
The main functionallity has been solved but there is still room to improve:
- multithread to shorten time
- make sure to include exceptions
- validate user inputs
- add Firefox and Safari functionallity (not sure if Safari allows headless state)

### Credits
https://smithio.medium.com/scraping-airbnb-website-with-python-beautiful-soup-and-selenium-8ec86e327b6c
for giving me the idea and serve as guide