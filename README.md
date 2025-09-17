# Name Screening Application

## Overview
The **Name Screening Application** is a Flask-based web application designed to process and screen names using the Microsoft Translator API and NetReveal APIs. It allows users to input a name, translate it, generate an XML payload, and send it to an external service for further processing. The application displays the results in a user-friendly format, including a detailed HTML table for matches.

## Features
- **Name Translation**: Translates the input name to English using the Microsoft Translator API.
- **XML Generation**: Dynamically generates an XML payload based on user input.
- **API Integration**:
  - Retrieves an access token from the NetReveal API.
  - Sends the generated XML to the NetReveal `processMessage` API.
- **Result Display**:
  - Displays the translated name.
  - Shows the generated XML.
  - Presents the API response in a structured HTML table format.
- **User-Friendly UI**: Built with Bootstrap for a clean and responsive design.

## Prerequisites
- NetReveal environment
- Microsoft Azure Tranlation service. Details on how to set up this service can be found [Microsoft Azure Names Transliteration](https://netreveal.atlassian.net/wiki/x/NoBGJQ)
- Python 3.7 or higher
- Flask
- Required Python libraries:
  - `requests`
  - `xml.etree.ElementTree`
  - `minidom`
- Environment variables:
  - `TRANSLATOR_SUBSCRIPTION_KEY`: Your Microsoft Translator API subscription key.
  - `TRANSLATOR_REGION`: The region for your Microsoft Translator API (e.g., `uaenorth`).

## Installation, Configuration and startup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/name-screening.git
   cd name-screening
2. create a ".env" file and add your API subscription key
   ```bash
   TRANSLATOR_SUBSCRIPTION_KEY
   TRANSLATOR_REGION
3. start the servive by running:
   ```bash
   python app.py
4. the application will start at http://127.0.0.1:5001
