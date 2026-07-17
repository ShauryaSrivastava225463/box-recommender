

from .models import Box


def find_best_box(product):
    """
    Given a Product instance, return the cheapest Box that can hold it.
    Returns None if no box fits.
    """
    prod_dims = product.sorted_dimensions()  
    prod_weight = float(product.weight)

    candidates = []

    for box in Box.objects.all():
        box_dims = box.sorted_dimensions()  

        
        fits_size = all(
            prod_dims[i] <= box_dims[i]
            for i in range(3)
        )

        fits_weight = prod_weight <= float(box.max_weight)

        if fits_size and fits_weight:
            candidates.append(box)

    if not candidates:
        return None

    candidates.sort(key=lambda b: (float(b.cost), float(b.inner_length) * float(b.inner_width) * float(b.inner_height)))

    return candidates[0]
