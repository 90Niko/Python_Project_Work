from datetime import datetime

def validate_year(year: str | int, min_year: int = 1886, max_year: int = None) -> bool:
    """
    Prüft, ob das Jahr eine gültige Ganzzahl ist und im erlaubten Bereich liegt.
    Standardmäßig ist der Bereich von 1886 bis zum aktuellen Jahr.
    """
    try:
        year = int(year)  # Versuche, das Jahr in eine Ganzzahl umzuwandeln
        if max_year is None:
            max_year = datetime.now().year  # Nutze das aktuelle Jahr als obere Grenze
        return min_year <= year <= max_year # Prüfe, ob Jahr im Bereich liegt
    except (ValueError, TypeError):
        return False  # Ungültige Eingabe (z. B. Buchstaben) wird als falsch zurückgegeben


def validate_price(price: str | int) -> bool:
    """
    Prüft, ob der Preis eine Ganzzahl >= 0 ist.
    """
    try:
        return int(price) >= 0  # Preis in Ganzzahl umwandeln und prüfen, ob >= 0
    except (ValueError, TypeError):
        return False  # Bei ungültigem Wert False zurückgeben

def validate_mileage(mileage: str | int) -> bool:
    """
    Prüft, ob der Kilometerstand (Mileage) eine Ganzzahl >= 0 ist.
    """
    try:
        return int(mileage) >= 0  # Kilometerstand umwandeln und prüfen, ob >= 0
    except (ValueError, TypeError):
        return False  # Bei Fehlern False zurückgeben

def validate_required_fields(*fields: str) -> bool:
    """
    Prüft, ob alle übergebenen Felder nicht leer sind (mindestens ein Zeichen nach Strip).
    Nur Strings werden geprüft, andere Typen werden ignoriert.
    """
    return all(field.strip() for field in fields if isinstance(field, str))
    # all() gibt True zurück, wenn alle Felder nicht-leer sind
