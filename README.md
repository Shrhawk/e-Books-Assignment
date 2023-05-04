# eBooks

## Features

+ Python FastAPI Backend
+ SQLite Database
+ Pydantic Schemas Validation
+ Alembic for managing DB Migrations
+ Pytest for running tests

To use the application, follow the outlined steps:

Clone/Copy the code and create a virtual environment:
```shell
python -m venv env
source env/bin/activate
python -m pip install --upgrade pip
```
Install the modules listed in the `requirements.txt` file
```shell
pip install -r requirements.txt
```
Add the following variables to `.env` file according to your environment needs:
```shell
eBOOKS_DATABASE_URL="sqlite+aiosqlite:///./e_book.db"
TEST_eBOOKS_DATABASE_URL="sqlite:///./test_e_book.db"
ASYNC_TEST_eBOOKS_DATABASE_URL="sqlite+aiosqlite:///./test_e_book.db"
```
## Database Migrations
Database migrations are managed by the ```sqlalchemy``` package ```alembic```.

First install the package into your environment with

```pip install alembic```

After installing the alembic we need to initialize the alembic to our working project directory.

```alembic init alembic```

This will add some directories such as ```alembic``` and file ```alembic.ini```
We need to modify ```alembic.ini``` as follows

```sqlalchemy.url = <database_url>```

Now in ```env.py``` in our alembic folder, we have to make some changes. To detect auto changes by alembic we need to give our model path to ```env.py``` as follows

```
from model import Base
target_metadata = [Base.metadata]
```

Finally, create the migration script. You can use the ```--autogenerate``` option to generate migrations based on the metadata automatically. For the first migrations we will run the following command

```alembic revision --autogenerate -m "First commit"```

Since, the migrations are already created so migrate those changes to your DB using the following command

```alembic upgrade head```

Now after any changes to the db run the above two commands to sync the changes

## Start the Application

```shell
uvicorn app.app:app --reload
```

The server will start listens on port 8000 on address [http://127.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Tests
To run test, run the following command
```shell
pytest -vv -s
```
