# Python Assignment: FastAPI Candidates and Skills Management

This is a FastAPI project designed to manage candidates and their associated skills. It provides a set of RESTful endpoints for creating, retrieving, updating, and deleting candidate and skill data, as well as user registration and login functionalities. It also utilizes Celery and Redis for asynchronous task management, specifically for generating candidate reports in CSV format, and is containerized using Docker.

## Features

- **Candidate Management**
  - List all candidates
  - Create a new candidate
  - Retrieve details of a specific candidate
  - Delete a candidate
  - Filter candidates based on specific criteria
  - Generate reports for candidates (asynchronously)

- **Skill Management**
  - Create a new skill
  - Retrieve details of a specific skill
  - List all skills associated with a candidate
  - Update an existing skill
  - Delete a skill

- **User Management**
  - Register a new user
  - User login

- **Asynchronous Reporting**
  - Generate candidate reports in CSV format using Celery and Redis

- **Docker Support**
  - Containerization for easier deployment

## API Endpoints

### Candidates

- **List Candidates**
  - `GET /`
  - Response: `Page[CandidateReadSchema]`

- **Create Candidate**
  - `POST /`
  - Request Body: `CandidateSchema`
  - Response: `CandidateReadSchema`

- **Retrieve Candidate**
  - `GET /{candidate_id}`
  - Response: `CandidateReadSchema`

- **Delete Candidate**
  - `DELETE /{candidate_id}`
  - Response: `200 OK`

- **Filter Candidates**
  - `GET /all/`
  - Request Parameters: `Params`, `CandidateFilter`
  - Response: `Page[CandidateReadSchema]`

- **Generate Candidates Report**
  - `GET /generate-report/`
  - Response: `202 Accepted` (async task initiated)

### Skills

- **Create Skill**
  - `POST /skills/`
  - Request Body: `SkillSchema`
  - Response: `SkillReadSchema`

- **Retrieve Skill**
  - `GET /skills/{skill_id}`
  - Response: `SkillReadSchema`

- **List Skills by Candidate**
  - `GET /skills/candidate/{candidate_id}`
  - Response: `Page[SkillReadSchemaWithCandidateId]`

- **Update Skill**
  - `PUT /skills/{skill_id}/update`
  - Request Body: `SkillUpdateSchema`
  - Response: `200 OK`

- **Delete Skill**
  - `DELETE /skills/{skill_id}/delete/`
  - Response: `200 OK`

### User Management

- **Register User**
  - `POST /register`
  - Request Body: `UserSchema`
  - Response: `201 Created`

- **User Login**
  - `POST /login`
  - Request Body: `UserSchema`
  - Response: `200 OK`

## Installation

To get started with the project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sohailcs140/python_assignment.git
   cd python_assignment
   ```
2. **Install Poetry**:If you haven't already installed Poetry.
   ```bash
      pip install poetry
   ```
3. **Install dependencies:**
   ```bash
      poetry install
   ```

4. **Set up Redis and Celery:**
   1. **Install Redis**
        ```bash
          sudo apt update
          sudo apt install redis-server
        ```
   2. **Start Redis**
      ```bash
      redis-server
      ```

5. **Run the Celery worker:**
   In a new terminal, start the Celery worker:
   ```bash
   celery -A app.celery.tasks worker
   ```
    Also Run flower for task Monitoring:
    ```bash
   celery -A app.celery.tasks flower
    ```

6. **Run the application:**
   ```bash
   fastapi dev app/main.py

   ```

7. **(Optional) Run with Docker:**
   If you prefer to run the application using Docker, you can build and run the container:
   ```bash
   docker-compose up --build
   ```

## Usage

After starting the server, you can access the API at `http://127.0.0.1:8000/`. You can use tools like [Postman](https://www.postman.com/) or [cURL](https://curl.se/) to interact with the endpoints.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/) for ORM capabilities.
- [Celery](https://docs.celeryproject.org/en/stable/) for task management.
- [Redis](https://redis.io/) for message brokering.
```
