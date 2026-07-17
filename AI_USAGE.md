 AI Usage Report

 1. Which AI Tool(s) I Used

Replit AI Agent** (Claude-based) — used within the Replit IDE to scaffold the project structure and generate initial file content.

---
 2. The Prompts I Gave

Prompt 1 (main request):
> We operate an ecommerce platform. When a customer places an order, the warehouse team needs to know which shipping box should be used. Each product has dimensions and weight. Each box has internal dimensions, maximum weight capacity, and cost. Design and build a small Django-based system that recommends the most suitable box for an order.
> Please keep it simple and understandable. My submission must show my own thinking.

Prompt 2 (clarification on algorithm):
> Use simple dimension comparison. Sort both the product dimensions and the box inner dimensions from smallest to largest, then compare them pairwise. Pick the cheapest box that fits.

---

3. What Output I Accepted

- The overall project folder structure (`box_recommender/`, `shipping/` app).
- The Django `settings.py` boilerplate (installed apps, database config, DRF config).
- The `Product` and `Box` model field definitions — the field names and types matched exactly what I had in mind.
- The skeleton of the REST API views (GET list, POST create, POST recommend).
- The basic test file structure using `TestCase` and `APIClient`.



 4. What Output I Rejected or Modified

-Algorithm explanation in `services.py`**: The AI used a more complex "itertools permutations" approach to check all 6 rotations of the product. I replaced this with the simpler "sort both dimension lists and compare" approach, which is easier to understand and equally correct.
- Serializer design**: The AI initially created a single combined serializer for the recommendation response. I split it into `RecommendBoxRequestSerializer` (input) and a plain dict response, which is easier to follow.
- Test cases: The AI generated 5 basic tests. I added 14 more tests myself to cover edge cases — exact-fit, over-limit weight, same-cost tiebreaker, rotated dimensions, and all API error paths (400, 404, missing fields).
- Admin registration: The AI did not register models in `admin.py`. I added `@admin.register` decorators with `list_display` and `ordering` so the admin panel is actually useful.
- Seed data command: The AI did not generate this. I wrote `management/commands/seed_data.py` myself to make it easy to demo the system.

---

 5. Mistakes the AI Made

1. Wrong algorithm: The AI used `itertools.permutations` to generate all 6 orientations of the product dimensions. While mathematically correct, it is over-engineered. The sorting trick (`sorted()` on both sides) is simpler, clearer, and reaches the same answer.

2. No seed data: The AI did not provide any way to load sample products and boxes, so the API would return empty results out of the box. I had to write the management command myself.

3. Missing edge case tests: The AI's initial test suite did not test weight-at-exactly-the-limit, weight-one-unit-over-limit, or cost tiebreakers. These are important boundary conditions that any real warehouse system would face.

4. Generic model `__str__`: The AI returned just `self.name` for `__str__`. I extended it to include dimensions and weight so the admin panel and shell are more informative.

---

 6. How I Verified the Final Code

1. Ran all 19 tests with `python manage.py test shipping --verbosity=2` and confirmed all passed (see `TEST_OUTPUT.md`).
2. Started the dev server (`python manage.py runserver`) and manually tested each endpoint with `curl`:
   - `POST /api/products/` to create a product.
   - `POST /api/boxes/` to create several boxes of different sizes and costs.
   - `POST /api/recommend/` with the product id to verify the cheapest fitting box was returned.
   - `POST /api/recommend/` with a very large product to verify the "no box found" response.
3. Loaded seed data (`python manage.py seed_data`) and ran the recommendation against all seeded products to manually inspect results.
4. Checked the admin panel at `/admin/` to confirm products and boxes are listed correctly with all fields.
5. Read through every file to make sure the code is readable and matches my own understanding of the logic — not just AI-generated text I don't understand.
