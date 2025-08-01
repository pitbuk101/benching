# Asynchronous Generative AI Normalization Service

This module provides a standalone, containerized FastAPI service that normalizes procurement data. It operates asynchronously: an API call triggers a background job that fetches data from an **S3 bucket**, processes it using a configurable LLM workflow, and uploads the result to a **Snowflake data warehouse**.

## Key Features

-   **Asynchronous Processing**: The API responds instantly (`202 Accepted`) while the heavy lifting happens in the background.
-   **S3 Input**: Fetches the source data (CSV or Excel) from a specified folder in an S3 bucket.
-   **Snowflake Output**: Loads the final, clean data directly into a Snowflake table.
-   **Dynamic & Idempotent**: Uses a `workspace_id` to create unique, overwritable tables in Snowflake (`NORMALIZED_{WORKSPACE_ID}`), making jobs safely re-runnable.
-   **Containerized**: Fully configured to run with Docker and Docker Compose.
-   **Secure**: All credentials and sensitive configurations are loaded from environment variables.


## Setup and Execution

### 1. Environment Variables

Create a `.env` file in the project root by copying `.env.example`. Fill in all the required credentials.

### 2. Running with Docker (Recommended)

From the `normalization_module` root directory, run:
```bash
docker-compose up --build
```

## API Usage

Access the interactive documentation at `http://localhost:8000/docs`.

* **Endpoint**: `POST /normalize/`
* **Request Body**: `application/json`
    -   `workspace_id` (string, required): A unique ID for the workspace (e.g., `1234_TestId`). This determines the final table name in Snowflake.
    -   `folder_id` (string, required): The folder path (key) in your S3 bucket where the input file is located (e.g., `templates`).

* **Example `curl` Request**:

    ```bash
    curl -X 'POST' \
      'http://localhost:8000/normalize/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
        "workspace_id": "1234_TestId",
        "folder_id": "templates"
      }'
    ```

* **Successful Response (`202 Accepted`)**:
    The API immediately responds, confirming the job has been queued.

    ```json
    {
      "status": "Accepted",
      "message": "Normalization job has been queued and will be processed in the background.",
      "workspace_id": "1234_TestId",
      "s3_folder_id": "templates"
    }
    ```
    ```json
    {
        "status": "Accepted",
        "message": "Benchmarking job has been queued and will be processed in the background.",
        "workspace_id": "90417221-5f60-4079-bcc0-433deb85b89f",
        "s3_path": "s3://sai-genai-data-export/web_scrapping/www.rakuten.com/Www.rakuten.com_20250627_125305.csv"
    }
    ```
    
* **Monitoring**: The status of the background job can be monitored by checking the log files generated in the `./logs/` directory.
* **Output**: The final, normalized data will be available in Snowflake in the schema NORMALIZED and table `NORMALIZED_1234_TestId`.

