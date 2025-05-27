def validate_year(year: str | int, min_year: int = 1886, max_year: int = 2026) -> bool:
    try:
        year = int(year)
        return min_year <= year <= max_year
    except (ValueError, TypeError):
        return False

def validate_price(price: str | int) -> bool:
    try:
        return int(price) >= 0
    except (ValueError, TypeError):
        return False

def validate_mileage(mileage: str | int) -> bool:
    try:
        return int(mileage) >= 0
    except (ValueError, TypeError):
        return False

def validate_required_fields(*fields: str) -> bool:
    return all(field.strip() for field in fields if isinstance(field, str))
