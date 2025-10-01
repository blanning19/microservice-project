# microservice-project

A multi-container Docker application that processes CSV files to calculate product totals through a secure, validated API workflow.

## Overview

This application consists of two Flask microservices that work together to:
- Validate and sanitize user input
- Process CSV files to calculate product totals
- Provide secure API endpoints for data retrieval

## Architecture

### ms-main (Input Validator) - Port 6000
- **Purpose**: Validates user input and file existence
- **Function**: Acts as a gateway, ensuring only valid requests reach the processing service
- **Validation**: Checks JSON format, file existence, and input sanitization

### ms-lookup (Data Processor) - Port 5002
- **Purpose**: Processes CSV files and calculates product totals
- **Function**: Reads CSV data, sums amounts for specified products
- **Output**: Returns calculated totals or appropriate error messages

## Application Flow

```
sequenceDiagram
    participant User
    participant ms-main as main (Validator)<br/>Port 6000
    participant ms-lookup as lookup (Processor)<br/>Port 5002
    participant CSV as CSV Files<br/>(Mounted Volume)

    User->>main: POST /calculate<br/>{"file": "Book1.csv", "product": "wheat"}
    
    main->>main: Validate JSON format
    main->>main: Check file existence<br/>/etc/data/Book1.csv
    
    alt File exists and valid
        main->>lookup: POST /<br/>{"file": "Book1.csv", "product": "wheat"}
        lookup->>CSV: Read CSV file
        CSV-->>lookup: Return data rows
        lookup->>lookup: Calculate sum for "wheat"
        lookup-->>main: {"file": "Book1.csv", "sum": 30}
        main-->>User: {"file": "Book1.csv", "sum": 30}
    else File not found or invalid
        main-->>User: {"file": "Book1.csv", "error": "File not found."}
    end
```

## API Usage

### Endpoint: `POST /calculate`
```json
{
  "file": "Book1.csv",
  "product": "wheat"
}
```

### Response Examples
```json
// Success
{
  "file": "Book1.csv",
  "sum": 30
}

// Error
{
  "file": "Book1.csv",
  "error": "File not found."
}
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd microservice-project
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Test the API**
   ```bash
   curl -X POST http://localhost:6000/calculate \
     -H "Content-Type: application/json" \
     -d '{"file": "Book1.csv", "product": "wheat"}'
   ```

## Data Format

CSV files should contain:
- Header row: `product,amount`
- Data rows: product name and numeric amount

## Technical Stack

- **Containerization**: Docker, Docker Compose
- **Backend**: Python, Flask
- **Communication**: REST APIs, HTTP requests
- **Data Processing**: CSV parsing, JSON responses

## Security Features

- Input validation and sanitization
- File existence verification
- Error handling for malformed data
- Container isolation for enhanced security