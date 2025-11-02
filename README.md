# INEGI Sanctions Scraper (Selenium + Scrapy)

Automated scraper that collects **sanctioned suppliers ("proveedores sancionados")** from the official [INEGI website](https://www3.inegi.org.mx/sistemas/ci/relps/) using **Selenium** and **Scrapy**, and updates a structured JSON file (`sanctions.json`) every 4 hours via **GitHub Actions**.

---

## Overview

This project automates the extraction of public sanction data published by INEGI (Mexico’s National Institute of Statistics and Geography).  
The spider navigates dynamically rendered content using Selenium, extracts supplier names and sanction numbers, and outputs them as clean, structured JSON.

Every 4 hours, the scraper runs automatically on **GitHub Actions**, regenerates the JSON file, and commits it back to the repository if any updates are detected.

---

## Project Structure

inegi/<br />
└── .github/<br />
│    └── workflows/<br />
│       └── run_scraper.yml # GitHub Actions automation<br />
├── inegi/<br />
│ ├── spiders/<br />
│ │ └── inegi_spider.py # Main Scrapy spider (with Selenium logic)<br />
│ │ <br />
│ ├── items.py # Defines scraped item structure<br />
│ ├── middlewares.py<br />
│ ├── pipelines.py # Saves and formats JSON output<br />
│ └── settings.py # Scrapy configuration<br />
│<br />
├──.gitignore<br />
├──main.py # Script to run the spider locally<br />
├──requirements.txt<br />
├──sanctions.json # Automatically updated data output<br />
├──scraper.yaml # Target URL and search parameters<br />
└── scrapy.cfg # Scrapy project configuration<br />


## How It Works<br />

1. **Selenium** launches a headless Chrome browser and loads the INEGI sanctions page.  
2. The spider searches for the configured term (from `scraper.yaml`), e.g. `"Ver total de proveedores sancionados"`.
3. Each sanction record is opened and parsed, extracting:
   - Entity name (`Entity_name`)
   - Sanction number(s) (`Sanction_numbers`)
4. **Scrapy Pipelines** save all results into a formatted JSON file:
   ```json
   [
     {
       "last_updated": "2025-11-02 10:45:11 UTC"
     },
     {
       "Entity_name": "ASHANTY FERNANDEZ MARTINEZ",
       "Sanction_numbers": ["40.902.05/8/2013"]
     }
   ]


GitHub Actions runs every hour, regenerates the file, and commits it automatically if changes occur.

## Requirements

Python ≥ 3.10
Google Chrome + ChromeDriver (for local runs)

Dependencies:
pip install scrapy selenium pyyaml

# Run the spider manually
python main.py

## GitHub Actions Automation

The workflow file .github/workflows/run_scraper.yml runs hourly:

on:
  schedule:
    - cron: "0 * * * *"
  workflow_dispatch:


# Each run:

Sets up Python
Installs dependencies
Runs the scraper in headless mode
Updates sanctions.json
Commits and pushes updates back to the main branch
