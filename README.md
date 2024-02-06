# SRM Time Table App

Welcome to the SRM Time Table App! This Flask-based web application allows users to submit and query time table data. The application uses Flask as the web framework, pandas for data manipulation, and Jinja for rendering templates.

## Features

- **Submit Form**: Users can submit time table data using a form.
- **Search Form**: Users can search for time table data based on various parameters.
- **CSV Download**: The submitted time table data can be downloaded as a CSV file.

## Project Structure

The project is organized into the following main components:

- **`timeTable` Module**: Contains the core functionality of the time table application.
  - `fileQuery.py`: Handles querying of time table data from a CSV file.
  - `pages.py`: Defines routes and views using Flask.

- **`static` Folder**: Contains static assets such as CSS stylesheets and JavaScript files.

- **`templates` Folder**: Contains HTML templates used by Flask for rendering views.

## Setup

1. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
2.Run command for the project:
    flask --app timeTable.app  run
## Run the Flask application
python -m flask run

This project is licensed under the MIT License.

You can customize this README based on your specific project details and add any additional sections that you find necessary.
