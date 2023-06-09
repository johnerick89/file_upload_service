## File Upload Service
The file_upload_service is an API Build a REST API for uploading a file with billions of records and processing the data to save users

## Requirements
- Python 3.10 or higher
- Django 3.1.0 or higher
- djangorestframework 3.11.0 or higher
- requests 2.25.0 or higher

## Setup
To set up and run the file_upload_service, follow these steps:

1. Clone the repository: `$ git clone https://github.com/johnerick89/file_upload_service.git`
2. Navigate into the project directory: `$ cd file_upload_service`
3. Create a new virtual environment (optional): `$ python3 -m venv env`
4. Activate the virtual environment: `$ source env/bin/activate` (Linux/MacOS) or `$ env\Scripts\activate` (Windows)
5. Create a `.env` file from the `.env.example` file provided with your own database and redis credentials.
6. Install the dependencies: `$ pip install -r requirements.txt`
7. Run the migrations: `$ python3 manage.py migrate`
8. Install redis in a terminal by running `$ sudo apt install redis` then start it by running: `$ redis-server`

Alternatively, you could use docker for running the app, in which case you can skip all these setup steps




## Usage
To start the Django development server, run the following command: `$ python3 manage.py runserver` 
or if you prefer to use docker then you could skip the setup above and just run `$ docker-compose up -d`

The API will be available at `http://127.0.0.1:8000/`. 
You can access the Django admin panel at `http://127.0.0.1:8000/admin/`.

## Endpoints
- `GET /users`: Returns a list of all users, allows for searching, sorting and filtering.
- `GET /file_uploads`: Returns a list of all file uploads done
- `POST /file_uploads`: Initiates a new file upload process. Allowed file formats as at now are `xls, xlsx, xml, csv, json and txt` and the key is `file`


## Running tests
You can run the tests by executing `$ python3 manage.py test` or to run a particular suite you can run `$ python3 manage.py test tests.test_tasks`

To run tests with coverage, run `$ coverage run --source='.' manage.py test tests`


## API Documentation

API documentation can be accessed using three different URLs:
- `http://127.0.0.1:8000/docs/` to access basic API documentation without much details on params and body
- `http://127.0.0.1:8000/swagger` to access detailed swagger API documentation with details on params and body
- `http://127.0.0.1:8000/redoc` to access detailed redoc API documentation with details on params and body


## Contributing
If you find a bug or would like to contribute to the project, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.