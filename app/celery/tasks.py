import csv
import os
from uuid import uuid1

from celery import Celery
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Candidate

load_dotenv()

app = Celery(
    __name__,
    broker=os.getenv('CELERY_BROKER_URL'),
    backend=os.getenv('CELERY_RESULT_BACKEND')
)

app.conf.broker_connection_retry_on_startup = True

OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.task
def generate_candidates_csv_file() -> str:
    """
    Generate a CSV file containing candidate information.

    This function retrieves all candidates from the database and writes
    their details to a CSV file, including their ID, name, email,
    skills, and experience. The CSV file is saved in the specified output
    directory with a unique filename.

    :return: The file path of the generated CSV file.

    :raises Exception: If there is an issue with database access or file
                     writing.
    """
    db: Session = next(get_db())
    candidates = db.query(Candidate).all()
    file_name = f"candidates__{str(uuid1().int)[:8]}.csv"
    csv_file_path = os.path.join(OUTPUT_DIR, file_name)

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(["id", "name", "email", "skills", 'experience'])
        print(candidates)
        for candidate in candidates:
            writer.writerow([candidate.id, candidate.name, candidate.email, [skill.name for skill in candidate.skills],
                             candidate.experience])

    return csv_file_path
