<div align="center">
  <a href="https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db">
    <img src="excel_db_logo.jpg" width="200">
  </a>
  <br>
  <h1>$${\color{lightgreen}\textsf{ Excel DB Database Systems Project: RUMAD 2.0}}$$</h1>
</div>

<h3 align="center">A new version of rumad.upr.edu by students for students.</h3>

## Table of Contents
- [Objectives](#objectives)
- [Project Overview](#project-overview)
- [Production Database Credentials](#production-database-credentials)
- [Getting Started](#getting-started)
  - [Local Setup](#local-setup)
- [How to Run the Frontend](#how-to-run-the-frontend)
- [Contributors](#contributors)

# Objectives
1. Understand the design, implementation and use of an application backed by a database system. 
2. Understand the use of table diagram for database application design. 
3. Gain experience by implementing applications using layers of increasing complexity and complex data structures.
4. Gain further experience with Web programming concepts including REST.
5. Gain experience with vector database and Langchain for AI chatbot implementation. 

# Project Overview 
You will design, implement, and test the backend of an application based on RUMAD to view sections 
and learn about the course. The data in the application is managed by a relational database system and 
exposed to client applications through a REST API. You will build the database application and REST 
API using Flask, which forms the system’s backend. Your database engine must be PostgreSQL (14 or 
higher), and you must implement the code in Python. The backend site will provide the user with the 
features specified in this document. In addition, your solution will offer a Web-based dashboard using 
Streamlit and an AI agent using Ollama using the tool provided in a later phase indicating relevant 
statistics.  . 

# Production Database Credentials

``` bash
host=cbdhrtd93854d5.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com
user=ufm5iffjti843g
database=dc79t7ga9hc6ud
password=p714ce504f5566ea5085651f4627a98521b24b94298c88546efee8a7e038ad933

port=5432
URI=postgres://ufm5iffjti843g:p714ce504f5566ea5085651f4627a98521b24b94298c88546efee8a7e038ad933@cbdhrtd93854d5.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dc79t7ga9hc6ud
```

### Heroku CLI
    heroku pg:psql postgresql-animate-40855 --app rumad-v2-app-excel-db

To access the front-end of the application, use the following link:
```bash
rest_api_host=https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db
```

# Getting Started

## Local Setup

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

# How to Run the Frontend:

First, download ollama in your local machine: https://ollama.com/

### Step 1: Run Ollama

To run Ollama locally, open a terminal and execute: 

```bash
  run ollama serve
```
### Step 2: Run the Frontend 
To run the frontend, navigate to the view directory in your terminal. Then, execute the following command:

 ```bash
  streamlit run app.py
```
### Frontend Options: Local or Rmeote
In the frontend, on the chatbot page, you have two options: run the chatbot locally or remotely.

#### To run the chatbot remotely:

- You need to be connected to RUMNET or RUMNETEP inside the Stefani Building.

- Alternatively, you can use a VPN. To request VPN access, please contact luis.lugo11@upr.edu. (Note: You only need to have the VPN running.)

#### To run the chatbot locally:

- Enable the local option in the frontend.

- Ensure that all required dependencies are installed beforehand.

## Contributors:
- Alanis Negroni Santiago 
- Anthony Manzano Echevarria
- Glerysbeth Serrano Flores
- Glorián M. Serrano Ortiz
- Edimar Valentín Kery

----------

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/jqhbANi7)
