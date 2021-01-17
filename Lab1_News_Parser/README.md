# Lab 1. News Parser

This folder contains a code to parse news articles from bbc.com website.

## Installation
1. Follow the instruction from root [README.md](../README.md)
2. Install requirements
`pip install -r requirements.txt`

## Usage
**Note:** Due to techinal issues, it may require several attempts to start parsing.

Run `python main.py`
```
usage: Scrapper for bbc.com [-h] [--driver-path DRIVER_PATH] [--headless]
                            [--save-path SAVE_PATH] [--min-news MIN_NEWS]
                            [--topic-indices N [N ...]]

optional arguments:
  -h, --help            show this help message and exit
  --driver-path DRIVER_PATH, -dp DRIVER_PATH
                        Path to driver
  --headless            Launch driver in background mode (no gui)
  --save-path SAVE_PATH, -sp SAVE_PATH
                        Path to the folder for saving the results into
  --min-news MIN_NEWS, -mn MIN_NEWS
                        Collect N news if possible (we can run out of
                        available page news). The actual number can be bigger
                        as we'll iterate the whole news page
  --topic-indices N [N ...], -ti N [N ...]
                        Indices of topics to aggregate news from (1-indexed)
```
