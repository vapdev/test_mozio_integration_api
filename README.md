# API Integration Developer Test for Mozio

This repository contains the code for the API Integration Developer test for the Mozio job application process.

## Requirements

- Python 3.6 or higher

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/vapdev/test_mozio_integration_api.git
    cd test_mozio_integration_api
    ```

2. Create and activate a virtual environment

    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```
    
    pip install -r requirements.txt
    ```

## Running the Script
To run the Python script that interacts with the Mozio API, follow these steps:

1. Set up the required configuration:

    - Replace the values of URL, HEADERS, SEARCH_PARAMS, and PASSENGER with the appropriate values for your environment.

2. Execute the script

    ```
    python main.py
    ```

This will start the search process, poll for results, make a reservation, get the provider, poll for reservation status, and cancel the reservation if needed.