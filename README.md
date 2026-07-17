# Box Recommender — Django Shipping Box Recommendation System

A Django + Django REST Framework application that recommends the cheapest suitable shipping box for a given product, based on dimensions and weight.

Built as a technical submission demonstrating Python, REST API design, business logic separation, and test-driven development.

---

 Table of Contents

1. [What It Does](#what-it-does)
2. [How to Run (Automated)](#how-to-run-automated)
3. [How to Run (Manual)](#how-to-run-manually-step-by-step)
4. [Project Structure](#project-structure)
5. [File-by-File Explanation](#file-by-file-explanation)
6. [Algorithm](#algorithm)
7. [API Endpoints & Examples](#api-endpoints--examples)
8. [Running the Tests](#running-the-tests)
9. [Django Admin Panel](#django-admin-panel)
10. [Tech Stack](#tech-stack)
11. [What I Learned](#what-i-learned)

---

What It Does

When a warehouse team receives an order, they need to know which shipping box to use.
This system:

1. Stores Products with dimensions (length × width × height in cm) and weight (kg).
2. Stores Boxes with internal dimensions, maximum weight capacity, and cost.
3. On request, finds every box where the product fits by size and weight, then returns the cheapest one.

If no box fits, the API says so clearly and suggests adding a larger box.


How to Run (Automated)

Two scripts are provided to automate the entire setup — one for each operating system.

Requirement: Python 3.8 or higher must be installed. Check with `python3 --version` (Mac/Linux) or `python --version` (Windows). Download from https://www.python.org/downloads/ if needed.

 On Mac / Linux

```bash
cd box_recommender_project
bash start.sh
```
 On Windows

Open Command Prompt (`cmd.exe`) — not PowerShell — then:

```bat
cd box_recommender_project
start.bat
```

**What the script does automatically (in order):**

| Step | What happens |
|------|-------------|
| 1 | Creates a Python virtual environment (`venv/`) |
| 2 | Installs `django` and `djangorestframework` from `requirements.txt` |
| 3 | Applies database migrations (creates `db.sqlite3`) |
| 4 | Loads 5 sample boxes + 6 sample products via `seed_data` command |
| 5 | Opens `http://127.0.0.1:8000/` in your browser automatically |
| 6 | Starts the development server |

The server runs until you press **Ctrl + C**.

Once running, open **http://127.0.0.1:8000/** to see the interactive demo page where you can add products, add boxes, and get recommendations live.

---

## How to Run Manually (Step by Step)

If you prefer to run each step yourself:

```bash

cd box_recommender_project


python3 -m venv venv
source venv/bin/activate        


pip install -r requirements.txt


python manage.py migrate


python manage.py seed_data

python manage.py createsuperuser

python manage.py runserver
```

The API is now available at: `http://127.0.0.1:8000/`
The admin panel is at: **`http://127.0.0.1:8000/admin/`**

 `shipping/models.py`
Defines two database tables:

- **`Product`** — name, length, width, height (cm), weight (kg). Has a helper method `sorted_dimensions()` that returns `[small, medium, large]` — used by the recommendation logic.
- **`Box`** — name, inner_length, inner_width, inner_height (cm), max_weight (kg), cost. Also has `sorted_dimensions()`.

---

### `shipping/services.py`
The core recommendation algorithm — isolated from HTTP so it can be tested directly.

`find_best_box(product)`:
1. Sorts the product's dimensions smallest → largest.
2. For every box in the database, sorts its inner dimensions the same way.
3. Checks: does every sorted product dimension fit inside the matching sorted box dimension? Does the product's weight fit?
4. Collects all boxes that pass. Returns the cheapest one (volume as tiebreaker). Returns `None` if nothing fits.

---

### `shipping/serializers.py`
Three DRF serializers:

- **`ProductSerializer`** — validates and shapes product data (id, name, length, width, height, weight).
- **`BoxSerializer`** — validates and shapes box data (id, name, inner dimensions, max_weight, cost).
- **`RecommendBoxRequestSerializer`** — validates the incoming `POST /api/recommend/` body (expects `product_id` as an integer).

---

### `shipping/views.py`
Three thin API views — they delegate all logic to serializers and services:

- **`ProductListCreateView`** — `GET /api/products/` and `POST /api/products/`.
- **`BoxListCreateView`** — `GET /api/boxes/` and `POST /api/boxes/`.
- **`RecommendBoxView`** — `POST /api/recommend/`. Validates the request, fetches the product, calls `find_best_box()`, and returns the result.

---

### `shipping/urls.py`
Maps the three views to URL paths under `/api/`.

---

### `shipping/admin.py`
Registers `Product` and `Box` with the Django admin panel. Adds `list_display`, `search_fields`, and `ordering` so the admin is actually useful — not just a blank page.

---

### `shipping/tests.py`
**22 automated tests** split into three groups:

| Group | Tests | What is covered |
|-------|-------|----------------|
| `FindBestBoxServiceTest` | 9 | Algorithm logic directly (no HTTP) |
| `ProductAPITest` | 4 | `GET` and `POST /api/products/` |
| `BoxAPITest` | 3 | `GET` and `POST /api/boxes/` |
| `RecommendBoxAPITest` | 6 | `POST /api/recommend/` — happy path + all error cases |

---

### `shipping/management/commands/seed_data.py`
A custom `manage.py` command that:
1. Clears the database.
2. Inserts 5 boxes (Extra Small → Extra Large) and 6 products (Coffee Mug, Laptop, Yoga Mat, Hardcover Book, Bicycle Helmet, Dumbbells Pair).
3. Prints a recommendation for each product so you can see the algorithm working immediately.

---

### `box_recommender/settings.py`
Standard Django settings. Key points:
- **SQLite** database — zero infrastructure needed.
- **`ALLOWED_HOSTS = ['*']`** — open for local development.
- **`REST_FRAMEWORK`** configured with `JSONRenderer` only (clean API responses).

---

### `requirements.txt`
Only two dependencies:
```
django>=5.0
djangorestframework>=3.14
```

---

## Algorithm

```
Product dims: length=10, width=20, height=5   →  sorted: [5, 10, 20]
Box dims:     inner_length=21, inner_width=6, inner_height=11  →  sorted: [6, 11, 21]

Check: 5 ≤ 6  ✓    10 ≤ 11  ✓    20 ≤ 21  ✓    weight ≤ max_weight  ✓
Result: FITS
```

Sorting both sets of dimensions before comparing automatically handles all product **orientations/rotations** — no need to check all 6 permutations manually. If the sorted product dims fit the sorted box dims, there is always a physical orientation that works.

Among all fitting boxes, the one with the **lowest cost** is returned. If two boxes cost the same, the one with the **smaller inner volume** wins (wastes less space).

---

## API Endpoints & Examples

### List all products
```
GET http://127.0.0.1:8000/api/products/
```
```json
[
  { "id": 1, "name": "Coffee Mug", "length": "12.00", "width": "10.00", "height": "14.00", "weight": "0.40" },
  { "id": 2, "name": "Laptop", "length": "38.00", "width": "26.00", "height": "3.00", "weight": "2.20" }
]
```

---

### Create a product
```
POST http://127.0.0.1:8000/api/products/
Content-Type: application/json

{
  "name": "Coffee Mug",
  "length": 12,
  "width": 10,
  "height": 14,
  "weight": 0.4
}
```
Response: `201 Created`

---

### List all boxes
```
GET http://127.0.0.1:8000/api/boxes/
```
```json
[
  { "id": 1, "name": "Extra Small Box", "inner_length": "15.00", "inner_width": "15.00", "inner_height": "10.00", "max_weight": "2.00", "cost": "0.80" },
  { "id": 2, "name": "Small Box", "inner_length": "25.00", "inner_width": "20.00", "inner_height": "15.00", "max_weight": "5.00", "cost": "1.50" }
]

 Create a box

POST http://127.0.0.1:8000/api/boxes/
Content-Type: application/json

{
  "name": "Small Parcel Box",
  "inner_length": 25,
  "inner_width": 20,
  "inner_height": 15,
  "max_weight": 5,
  "cost": 1.50
}
```
Response: `201 Created`

---
 Get a recommendation
```
POST http://127.0.0.1:8000/api/recommend/
Content-Type: application/json

{ "product_id": 1 }
```

Response — box found:
json
{
  "product": {
    "id": 1,
    "name": "Coffee Mug",
    "length": "12.00",
    "width": "10.00",
    "height": "14.00",
    "weight": "0.40"
  },
  "recommended_box": {
    "id": 1,
    "name": "Extra Small Box",
    "inner_length": "15.00",
    "inner_width": "15.00",
    "inner_height": "10.00",
    "max_weight": "2.00",
    "cost": "0.80"
  },
  "message": "Box 'Extra Small Box' is recommended for product 'Coffee Mug'."
}
```

Response — no box fits:
```json
{
  "product": { "id": 3, "name": "Yoga Mat", ... },
  "recommended_box": null,
  "message": "No suitable box found for product 'Yoga Mat'. Consider adding a larger box."
}
```

---

Quick curl examples

```bash

curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Coffee Mug","length":12,"width":10,"height":14,"weight":0.4}'


curl -X POST http://127.0.0.1:8000/api/recommend/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'
```

---

 Running the Tests

bash
Make sure your virtual environment is active first
source venv/bin/activate   # Windows: venv\Scripts\activate

python manage.py test shipping --verbosity=2
```

Expected result: **22 tests, 0 failures, 0 errors** (see `TEST_OUTPUT.md` for the full output).

Tests are fully isolated — each test case creates its own in-memory SQLite database and cleans up after itself. No seed data or manual setup needed.

---

Django Admin Panel

1. Create a superuser (if you haven't yet):
   ```bash
   python manage.py createsuperuser
   ```
2. Start the server and visit: `http://127.0.0.1:8000/admin/`
3. Log in with the credentials you just created.
4. You can add, edit, and delete Products and Boxes through the web interface.


 What I Learned

1. Sorting dimensions is a clean, simple way to handle all product orientations — if both sets of dimensions are sorted the same way, a single element-by-element comparison covers every possible rotation.

2. Django REST Framework serializers are a good place to put input validation. Keeping that validation out of views makes views thin and easy to read.

3. Separating business logic (`services.py`) from HTTP handling (`views.py`) makes the algorithm testable without any HTTP overhead — you pass in a model instance and get back a result.

4. SQLite is perfectly adequate for a self-contained warehouse tool and requires zero infrastructure to set up or run.
