from django.db import models


class Product(models.Model):
    """
    A product that needs to be shipped.
    Dimensions are in centimetres, weight in kilograms.
    """
    name = models.CharField(max_length=200)
    length = models.DecimalField(max_digits=8, decimal_places=2, help_text="Length in cm")
    width  = models.DecimalField(max_digits=8, decimal_places=2, help_text="Width in cm")
    height = models.DecimalField(max_digits=8, decimal_places=2, help_text="Height in cm")
    weight = models.DecimalField(max_digits=8, decimal_places=2, help_text="Weight in kg")

    def __str__(self):
        return f"{self.name} ({self.length}x{self.width}x{self.height} cm, {self.weight} kg)"

    def sorted_dimensions(self):
        """Return product dimensions sorted smallest→largest for easy comparison."""
        return sorted([float(self.length), float(self.width), float(self.height)])


class Box(models.Model):
    """
    A shipping box available in the warehouse.
    Internal dimensions are in centimetres, weight capacity in kg, cost in currency units.
    """
    name           = models.CharField(max_length=200)
    inner_length   = models.DecimalField(max_digits=8, decimal_places=2, help_text="Inner length in cm")
    inner_width    = models.DecimalField(max_digits=8, decimal_places=2, help_text="Inner width in cm")
    inner_height   = models.DecimalField(max_digits=8, decimal_places=2, help_text="Inner height in cm")
    max_weight     = models.DecimalField(max_digits=8, decimal_places=2, help_text="Max weight capacity in kg")
    cost           = models.DecimalField(max_digits=8, decimal_places=2, help_text="Cost of the box")

    def __str__(self):
        return f"{self.name} ({self.inner_length}x{self.inner_width}x{self.inner_height} cm, max {self.max_weight} kg, cost {self.cost})"

    def sorted_dimensions(self):
        """Return box inner dimensions sorted smallest→largest for easy comparison."""
        return sorted([float(self.inner_length), float(self.inner_width), float(self.inner_height)])
