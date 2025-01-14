import requests
from bs4 import BeautifulSoup
import json

def retrieve_and_display_message(url):
    # Fetch the HTML content of the Google Doc at the provided URL
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Locate the div containing the document's content
    document_content = soup.find('div', class_='doc-content')

    # Look for the first table within the document content
    table = document_content.find('table')

    # If a table is found, print its prettified version; otherwise, notify the user
    if table:
        print("Table found, displaying its structure:")
        print(table.prettify())
    else:
        print("No table found in the document.")

    # Prepare an empty list to store extracted coordinate and character data
    message_data = []

    # Extract and process rows, skipping the header row
    for row in table.find_all('tr')[1:]:  # Skipping the first row (header)
        columns = row.find_all('td')
        if len(columns) == 3:
            x = columns[0].get_text(strip=True)  # X coordinate
            char = columns[1].get_text(strip=True)  # Character
            y = columns[2].get_text(strip=True)  # Y coordinate

            # Store the extracted data as a dictionary in the list
            message_data.append({
                'x_coordinate': x,
                'character': char,
                'y_coordinate': y
            })
