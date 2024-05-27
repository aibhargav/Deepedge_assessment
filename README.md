# Smart visual inspection system

## Overview

This project implements a Visual Inspection System API using FastAPI, allowing users to perform CRUD (Create, Read, Update, Delete) operations on inspections from multiple inspection stations. The API supports filtering inspections by inspection station and product, as well as pagination for handling large numbers of inspections.

### Code Overview

The code structure includes:

- **Main File**: `app.py` contains the FastAPI application and endpoints.
- **Data Handling**: Functions for reading from/writing to JSON files.
- **Models**: Pydantic BaseModel for inspections.
- **Dependencies**: FastAPI, uvicorn, and pydantic.

### Installation

1. **Unzip the Project**:
   - Unzip the provided ZIP file to a directory of your choice.

2. **Navigate to Project Directory**:
   - Open your terminal or command prompt.
   - Change the directory to where you unzipped the project. For example:
     ```sh
     cd path/to/unzipped/project
     ```

3. **Create a Virtual Environment**:
   - Create a virtual environment to isolate project dependencies:
     ```sh
     python -m venv env
     ```
   - Activate the virtual environment:
     - On macOS/Linux:
       ```sh
       source env/bin/activate
       ```
     - On Windows:
       ```sh
       env\Scripts\activate
       ```

4. **Install Dependencies**:
   - Install the required dependencies listed in `requirements.txt`:
     ```sh
     pip install -r requirements.txt
     ```

### Running Locally

1. **Start the Development Server**

    ```bash
    uvicorn app:app --reload
    ```


### Docker Setup

1. **Build the Docker Image**

    ```bash
    docker build -t visual-inspection-system .
    ```

2. **Run the Docker Container**

    ```bash
    docker run -d -p 8000:80 visual-inspection-system
    ```



## Making API Calls

### 1. Create Inspections

- **Endpoint:** `POST /inspections/`
- **Description:** Create one or more inspections.
- **Request Body Format:** JSON array of Inspection objects.
  
    ```json
    [
        {
            "name": "Station A",
            "description": "Inspection for product A",
            "product": "Product A",
            "criteria": "Criteria A",
            "image_url": "http://example.com/image_a.jpg",
            "inspection_outcome": "pass"
        },
        {
            "name": "Station B",
            "description": "Inspection for product B",
            "product": "Product B",
            "criteria": "Criteria B",
            "image_url": "http://example.com/image_b.jpg",
            "inspection_outcome": "fail"
        }
    ]
    ```

### 2. Read Inspections

- **Endpoint:** `GET /inspections/`
- **Description:** Retrieve a list of inspections with optional filtering and pagination.
- **Query Parameters:** 
    - `skip` (int): Number of records to skip (default: 0)
    - `limit` (int): Maximum number of records to return (default: 10)
    - `inspection_station` (str): Filter by inspection station name
    - `product` (str): Filter by product name

    **Example URL with Filtering and Pagination:** `http://127.0.0.1:8000/inspections/`

### 3. Read Single Inspection

- **Endpoint:** `GET /inspections/{inspection_id}`
- **Description:** Retrieve a single inspection by its ID.

    **Example URL:** `http://127.0.0.1:8000/inspections/1`

### 4. Update Inspection

- **Endpoint:** `PUT /inspections/{inspection_id}`
- **Description:** Update an existing inspection by its ID.
- **Request Body Format:** JSON object containing the updated inspection fields.

    ```json
    {
        "name": "Updated Station A",
        "description": "Updated Inspection for product A",
        "product": "Updated Product A",
        "criteria": "Updated Criteria A",
        "image_url": "http://example.com/updated_image.jpg",
        "inspection_outcome": "fail"
    }
    ```

### 5. Delete Inspection

- **Endpoint:** `DELETE /inspections/{inspection_id}`
- **Description:** Delete an existing inspection by its ID.

    **Example URL:** `http://127.0.0.1:8000/inspections/1`



## Filtering Inspections


### Filtering by Inspection Station

- **Query Parameter:** `inspection_station`
- **Description:** Filters inspections by the name of the inspection station.
- **Example:** To retrieve inspections from "Station A", add `inspection_station=Station%20A` to the URL.

    **Example URL:** `http://127.0.0.1:8000/inspections/?inspection_station=Station%20B`

### Filtering by Product

- **Query Parameter:** `product`
- **Description:** Filters inspections by the product name.
- **Example:** To retrieve inspections for "Product A", add `product=Product%20A` to the URL.

    **Example URL:** `http://127.0.0.1:8000/inspections/?product=Product%20B`

## Pagination


### Pagination Parameters

- **Query Parameter:** `skip`
- **Description:** Number of records to skip (default: 0).
- **Query Parameter:** `limit`
- **Description:** Maximum number of records to return per page (default: 10).

### Example Pagination URL

To retrieve the first 5 inspections, you can use the following URL:

- **Example URL:** `http://127.0.0.1:8000/inspections/?skip=0&limit=5`
