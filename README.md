-----

# Museum Cultural Heritage Reconciliation Service

This is a Python-based reconciliation service built with Flask and SQLite, designed to help standardize and clean cultural heritage data. It follows the **W3C OpenRefine Reconciliation API specification**, making it compatible with tools like **OpenRefine**.

The service provides a local, self-contained database of prominent museums, artists, and artifacts. It uses **fuzzy matching** to accurately link and reconcile messy or incomplete data from your spreadsheets with the standardized information in its database.

## Key Features

  - **W3C Reconciliation API Compliance**: Fully compatible with OpenRefine and other data cleaning tools.
  - **Dedicated Database**: A pre-populated SQLite database containing structured data on cultural heritage entities.
  - **Fuzzy Matching**: Uses the `fuzzywuzzy` library to find the best possible matches for your data, even with misspellings or variations.
  - **Entity Types**: Supports reconciliation for several distinct entity types:
      - `Museum/Institution`
      - `Artist/Creator`
      - `Cultural Artifact`
      - `Culture/Period`
  - **Helper Endpoints**: Includes endpoints for **auto-completion**, **type suggestions**, and **entity previews** to enhance the user experience in OpenRefine.

-----

## Folder Structure

The project is organized into a clean and modular structure to separate concerns and improve maintainability.

```
museum-reconciliation-service/
├── app.py                          # Main application entry point
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration settings
├── data/
│   ├── museums.csv                 # Museums data
│   ├── artists.csv                 # Artists data
│   └── artworks.csv               # Artworks data
├── services/
│   ├── __init__.py
│   ├── database_service.py         # Database operations
│   ├── reconciliation_service.py   # Core reconciliation logic
│   └── search_service.py           # Search functionality
├── routes/
│   ├── __init__.py
│   ├── main_routes.py              # Main reconciliation routes
│   ├── api_routes.py               # API endpoints
│   └── preview_routes.py           # Preview and view routes
├── templates/
│   ├── museum_preview.ejs          # Museum preview template
│   ├── artist_preview.ejs          # Artist preview template
│   └── artifact_preview.ejs       # Artifact preview template
├── static/css/
│   └── preview.css                 # Shared CSS for previews
├── utils/
│   ├── __init__.py
│   └── text_utils.py               # Text processing utilities
├── requirements.txt                # Python dependencies
└── README.md                      # Project documentation
```

-----

## Installation and Setup

### Prerequisites

  - Python 3.7 or higher
  - `pip` (Python package installer)

### Steps

1.  **Clone the repository:**

    ```sh
    git clone <your-repo-url>
    cd museum-reconciliation
    ```

2.  **Create and activate a virtual environment:**
    It's recommended to create a dedicated environment to manage dependencies for this project.

    ```sh
    # On macOS and Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    py -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    The project uses a few key libraries, including `flask` for the web server and `fuzzywuzzy` for string matching.

    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    This command will start the Flask server and automatically create and populate the `museum_reconciliation.db` file in the `data/` directory.

    ```sh
    python app.py
    ```

    You should see the following output, indicating the service is running:

    ```
    ============================================================
    Museum Cultural Heritage Reconciliation Service
    ============================================================
    Service URL: http://localhost:5000/

    To use with OpenRefine:
    1. Start OpenRefine and load your cultural heritage data
    2. Select column > Reconcile > Start reconciling...
    3. Add Standard Service: http://localhost:5000/
    4. Select appropriate entity type (Artifact, Museum, Artist, etc.)

    Available entity types:
    - Cultural Artifact (paintings, sculptures, etc.)
    - Museum/Institution
    - Artist/Creator
    - Culture/Period
    ============================================================
    ```

-----

## Usage with OpenRefine

1.  **Open OpenRefine** and import your dataset.
2.  In the column you want to reconcile (e.g., a column of museum names or artwork titles), click the dropdown arrow, navigate to **Reconcile**, and select **Start reconciling...**.
3.  In the "Reconcile" dialog box, click **Add Standard Service...** and enter the URL: `http://localhost:5000/`.
4.  OpenRefine will detect the service. Select the appropriate **entity type** (`Museum/Institution`, `Cultural Artifact`, etc.) from the dropdown menu to improve matching accuracy.
5.  Click **Start Reconciling** to run the process.

The service will send back a list of potential matches for each cell, with a score and a `match` flag indicating the confidence level. You can then use OpenRefine's features to review and apply the reconciliation results.