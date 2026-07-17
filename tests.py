

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Product, Box
from .services import find_best_box



def make_product(name="Test Product", length=10, width=10, height=10, weight=1):
    return Product.objects.create(name=name, length=length, width=width, height=height, weight=weight)

def make_box(name, inner_length, inner_width, inner_height, max_weight, cost):
    return Box.objects.create(
        name=name,
        inner_length=inner_length,
        inner_width=inner_width,
        inner_height=inner_height,
        max_weight=max_weight,
        cost=cost,
    )




class FindBestBoxServiceTest(TestCase):

    def test_returns_none_when_no_boxes_exist(self):
        """No boxes in DB → returns None."""
        product = make_product()
        result = find_best_box(product)
        self.assertIsNone(result)

    def test_returns_none_when_product_is_too_large(self):
        """Product bigger than every box → returns None."""
        make_box("Tiny Box", 5, 5, 5, 10, 1.00)
        product = make_product(length=20, width=20, height=20, weight=1)
        result = find_best_box(product)
        self.assertIsNone(result)

    def test_returns_none_when_product_is_too_heavy(self):
        """Product fits by size but exceeds max_weight → returns None."""
        make_box("Weight-limited Box", 50, 50, 50, 1, 1.00)
        product = make_product(length=10, width=10, height=10, weight=5)
        result = find_best_box(product)
        self.assertIsNone(result)

    def test_returns_cheapest_box_that_fits(self):
        """Two boxes both fit — should pick the cheaper one."""
        cheap  = make_box("Small Cheap Box",  20, 20, 20, 10, 2.00)
        make_box("Large Expensive Box", 40, 40, 40, 10, 8.00)
        product = make_product(length=15, width=15, height=15, weight=1)
        result = find_best_box(product)
        self.assertEqual(result.id, cheap.id)

    def test_product_fits_when_dimensions_are_equal(self):
        """A product that is exactly the same size as the box should fit."""
        box = make_box("Exact Fit Box", 10, 10, 10, 5, 3.00)
        product = make_product(length=10, width=10, height=10, weight=5)
        result = find_best_box(product)
        self.assertEqual(result.id, box.id)

    def test_product_fits_rotated(self):
        """
        Product is 5x10x20 cm and box is 6x11x21 cm.
        After sorting dimensions, product [5,10,20] fits in box [6,11,21].
        """
        box = make_box("Rotated Fit Box", 21, 6, 11, 10, 4.00)
        product = make_product(length=10, width=20, height=5, weight=1)
        result = find_best_box(product)
        self.assertEqual(result.id, box.id)

    def test_expensive_fits_but_cheaper_doesnt(self):
        """Only the expensive box is big enough — must return the expensive one."""
        make_box("Small Box", 5, 5, 5, 10, 1.00)
        expensive = make_box("Large Box", 30, 30, 30, 10, 9.00)
        product = make_product(length=20, width=20, height=20, weight=1)
        result = find_best_box(product)
        self.assertEqual(result.id, expensive.id)

    def test_weight_exactly_at_limit_is_accepted(self):
        """Product weight equal to box max_weight should be accepted."""
        box = make_box("Exact Weight Box", 20, 20, 20, 3, 2.00)
        product = make_product(length=5, width=5, height=5, weight=3)
        result = find_best_box(product)
        self.assertEqual(result.id, box.id)

    def test_weight_over_limit_is_rejected(self):
        """Product weight one gram over max_weight should be rejected."""
        make_box("Over-limit Box", 20, 20, 20, 3, 2.00)
        product = make_product(length=5, width=5, height=5, weight=3.01)
        result = find_best_box(product)
        self.assertIsNone(result)

    def test_returns_smallest_volume_on_cost_tie(self):
        """Two boxes have same cost — should return the one with smaller volume."""
        small = make_box("Same-cost Small", 15, 15, 15, 10, 5.00)
        make_box("Same-cost Large",  25, 25, 25, 10, 5.00)
        product = make_product(length=10, width=10, height=10, weight=1)
        result = find_best_box(product)
        self.assertEqual(result.id, small.id)


# ─────────────────────────────────────────────
#  2. API endpoint tests
# ─────────────────────────────────────────────

class ProductAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_products_empty(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_product(self):
        data = {"name": "Book", "length": 30, "width": 20, "height": 3, "weight": 0.5}
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Book')

    def test_create_product_missing_field(self):
        """Missing 'weight' should return 400."""
        data = {"name": "Incomplete", "length": 10, "width": 10, "height": 10}
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_list_products_returns_all(self):
        make_product("Product A")
        make_product("Product B")
        response = self.client.get('/api/products/')
        self.assertEqual(len(response.json()), 2)


class BoxAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_boxes_empty(self):
        response = self.client.get('/api/boxes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_box(self):
        data = {
            "name": "Small Box",
            "inner_length": 20, "inner_width": 20, "inner_height": 20,
            "max_weight": 5, "cost": 1.50
        }
        response = self.client.post('/api/boxes/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Small Box')

    def test_create_box_missing_field(self):
        """Missing 'cost' should return 400."""
        data = {"name": "No Cost Box", "inner_length": 10, "inner_width": 10, "inner_height": 10, "max_weight": 5}
        response = self.client.post('/api/boxes/', data, format='json')
        self.assertEqual(response.status_code, 400)


class RecommendBoxAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_recommend_returns_404_for_unknown_product(self):
        response = self.client.post('/api/recommend/', {"product_id": 9999}, format='json')
        self.assertEqual(response.status_code, 404)

    def test_recommend_returns_400_for_missing_product_id(self):
        response = self.client.post('/api/recommend/', {}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_recommend_returns_none_when_no_box_fits(self):
        product = make_product("Giant Product", length=100, width=100, height=100, weight=100)
        make_box("Tiny Box", 5, 5, 5, 1, 1.00)
        response = self.client.post('/api/recommend/', {"product_id": product.id}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['recommended_box'])

    def test_recommend_returns_best_box(self):
        product = make_product("Small Item", length=10, width=10, height=10, weight=1)
        cheap = make_box("Cheap Box", 20, 20, 20, 5, 1.00)
        make_box("Expensive Box", 30, 30, 30, 5, 5.00)
        response = self.client.post('/api/recommend/', {"product_id": product.id}, format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['recommended_box']['id'], cheap.id)
        self.assertIn("recommended", data['message'].lower())

    def test_recommend_message_when_no_box_found(self):
        product = make_product("Huge Product", length=500, width=500, height=500, weight=500)
        response = self.client.post('/api/recommend/', {"product_id": product.id}, format='json')
        data = response.json()
        self.assertIsNone(data['recommended_box'])
        self.assertIn("No suitable box", data['message'])
