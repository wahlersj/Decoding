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
 # Convert the list of extracted data to a pretty-printed JSON string
    json_output = json.dumps(message_data, indent=4)
    print("Extracted data in JSON format:")
    print(json_output)

    # Sort the data based on X and Y coordinates
    sorted_data = sorted(message_data, key=lambda item: (int(item['x_coordinate']), int(item['y_coordinate'])))

    # Print the sorted data in JSON format
    print("\nSorted data:")
    print(json.dumps(sorted_data, indent=4, ensure_ascii=False))

    # Determine the size of the grid by finding the maximum X and Y coordinates
    grid_width = max(int(item['x_coordinate']) for item in sorted_data) + 1
    grid_height = max(int(item['y_coordinate']) for item in sorted_data) + 1

    # Initialize an empty grid with the calculated dimensions
    grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]

    # Place the characters in the grid at their corresponding X and Y positions
    for item in sorted_data:
        x = int(item['x_coordinate'])
        y = int(item['y_coordinate'])
        grid[grid_height - y - 1][x] = item['character']  # Flip Y axis to align with grid

    # Output the final grid as the secret message
    print("\nDecoded secret message (grid format):")
    for row in grid:
        print(''.join(row))

# Example usage with a Google Doc URL (replace with the actual URL as needed)
retrieve_and_display_message('https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub')
