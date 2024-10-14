# PostgreSQL Docker Setup

This repository contains a Docker setup for running a PostgreSQL database with predefined tables. Follow the instructions below to get the database running and connect to it using DataGrip.

## Prerequisites

Before you begin, ensure you have the following installed:

- Docker
- DataGrip 
## Getting Started

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/CIIC4060-ICOM5016-FALL-2024/rumad-v2-app-excel-db.git
cd rumad-v2-app-excel-db/postgres
git switch docker
```

### Running the Docker Container 
Build and Start the Container: Run the following command to start the PostgreSQL container in detached mode:

```bash
docker-compose up -d
```

Verify the Container is Running: Check if the container is running:
```bash
docker ps
```

## Connect to PostgreSQL with DataGrip
### Open Project
Open DataGrip
Open New Project
Go to Git -> Get From Version Control -> Paste the repo url

### Add Data Source
Add a New Data Source:
Go to File > Data Sources and Drivers.
Click on the + button and select PostgreSQL.

Configure Connection Settings:
- Host: localhost
- Port: 1234
- User: excel
- Password: password
- Database: excel_db

## Get Tables
Go to File -> Open -> postgres/table_scripts.sql
Run it and 6 table would be generated

## Stopping Docker
To stop the PostgreSQL container, run:
```bash
docker-compose down
```
