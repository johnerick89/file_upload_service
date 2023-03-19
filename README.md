## File Upload Service
The file_upload_service is an API Build a REST API for uploading a file with billions of records and processing the data to save users

## Requirements
- Python 3.10 or higher
- Django 3.1.0 or higher
- djangorestframework 3.11.0 or higher
- requests 2.25.0 or higher

## Setup
To set up and run the itunes-api-wrapper, follow these steps:

1. Clone the repository: `$ git clone https://github.com/johnerick89/file_upload_service.git`
2. Navigate into the project directory: `$ cd file_upload_service`
3. Create a new virtual environment (optional): `$ python3 -m venv env`
4. Activate the virtual environment: `$ source env/bin/activate` (Linux/MacOS) or `$ env\Scripts\activate` (Windows)
5. Install the dependencies: `$ pip install -r requirements.txt`
6. Run the migrations: `$ python3 manage.py migrate`



## Usage
To start the Django development server, run the following command: `$ python3 manage.py runserver`.

The API will be available at `http://127.0.0.1:8000/`. 
You can access the Django admin panel at `http://127.0.0.1:8000/admin/`.

## Endpoints
## Artists
- `GET /artists/`: Returns a list of all artists.
- `GET /artists/{id}/`: Returns a single artist with the specified ID.
- `POST /artists/`: Creates a new artist with the specified data.
- `PUT /artists/{id}/`: Updates the artist with the specified ID with the specified data.
- `DELETE /artists/{id}/`: Deletes the artist with the specified ID.

## Albums
- `GET /albums/`: Returns a list of all albums.
- `GET /albums/{id}/`: Returns a single album with the specified ID.
- `POST /albums/`: Creates a new album with the specified data.
- `PUT /albums/{id}/`: Updates the album with the specified ID with the specified data.
- `DELETE /albums/{id}/`: Deletes the album with the specified ID.

## Songs
- `GET /songs/`: Returns a list of all songs.
- `GET /songs/{id}/`: Returns a single song with the specified ID.
- `POST /songs/`: Creates a new song with the specified data.
- `PUT /songs/{id}/`: Updates the song with the specified ID with the specified data.
- `DELETE /songs/{id}/`: Deletes the song with the specified ID.

## Seeding
To seed the database, send a `POST` request to the `/seed/` endpoint with a JSON payload that looks like this:

`{
    "artists": ["Rihanna", "Nicki Minaj", "Coldplay", "50 Cent", ...]
}`
For every artist in the list, all their albums and songs will be seeded in the app database.

## Query Parameters
All endpoints that allow filtering support the following query parameters:

`search`: Filters by name, artist, or album name.
`artist`: Filters by artist name.
`album`: Filters by album name.
`genre_name`: Filters by genre name.

## Seeding the Database
To seed the database, send a POST request to the `/seed/` endpoint with a JSON payload that looks like this:

`{
    "artists": ["Rihanna", "Nicki Minaj", "Coldplay", "50 Cent", ...]
}`
For every artist in the list, all their albums and songs will be seeded in the app database.

## Contributing
If you find a bug or would like to contribute to the project, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.