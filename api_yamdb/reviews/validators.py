def score_validator(value):
    """Проверяет, что полученное значение находится в пределах от 0 до 10."""
    if value < 0 or value > 10:
        raise ValueError('Score must be between 0 and 10')
