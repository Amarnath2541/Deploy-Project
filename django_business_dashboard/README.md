# Search and Business Dashboard (Django Framework)

A full-featured Django implementation of a business dashboard featuring search, filters, pagination, ORM aggregations (`Sum`, `Count`, `Avg`, `annotate`), and visual Chart.js dashboards.

## Setup Instructions

1. Extract the ZIP file.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations to initialize the database:
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```
5. Open your browser and go to `http://127.0.0.1:8000/`.

The app will automatically populate initial sample business transaction records on first load.
