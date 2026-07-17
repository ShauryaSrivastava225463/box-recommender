"""
Management command to load sample products and boxes for demo/testing.

Usage:
    python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from shipping.models import Product, Box


class Command(BaseCommand):
    help = 'Load sample products and boxes into the database'

    def handle(self, *args, **options):
        # Clear existing data
        Product.objects.all().delete()
        Box.objects.all().delete()
        self.stdout.write("Cleared existing products and boxes.")

        # ── Sample Boxes ──────────────────────────────────────────────
        boxes = [
            Box(name="Extra Small Box",  inner_length=15, inner_width=15, inner_height=10, max_weight=2,  cost=0.80),
            Box(name="Small Box",        inner_length=25, inner_width=20, inner_height=15, max_weight=5,  cost=1.50),
            Box(name="Medium Box",       inner_length=40, inner_width=30, inner_height=25, max_weight=10, cost=2.50),
            Box(name="Large Box",        inner_length=60, inner_width=50, inner_height=40, max_weight=20, cost=4.00),
            Box(name="Extra Large Box",  inner_length=80, inner_width=70, inner_height=60, max_weight=30, cost=6.50),
        ]
        Box.objects.bulk_create(boxes)
        self.stdout.write(f"Created {len(boxes)} boxes.")

        # ── Sample Products ───────────────────────────────────────────
        products = [
            Product(name="Coffee Mug",      length=12, width=10, height=14, weight=0.4),
            Product(name="Laptop",          length=38, width=26, height=3,  weight=2.2),
            Product(name="Yoga Mat",        length=61, width=15, height=15, weight=1.5),
            Product(name="Hardcover Book",  length=28, width=21, height=4,  weight=0.8),
            Product(name="Bicycle Helmet",  length=30, width=28, height=22, weight=0.7),
            Product(name="Dumbbells Pair",  length=35, width=15, height=15, weight=10),
        ]
        Product.objects.bulk_create(products)
        self.stdout.write(f"Created {len(products)} products.")

        # ── Show recommendations ──────────────────────────────────────
        from shipping.services import find_best_box
        self.stdout.write("\n── Recommendations ─────────────────────────────────────────")
        for product in Product.objects.all():
            best = find_best_box(product)
            if best:
                self.stdout.write(f"  {product.name:20s} → {best.name} (cost: £{best.cost})")
            else:
                self.stdout.write(f"  {product.name:20s} → ❌ No suitable box found")
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Seed data loaded successfully."))
