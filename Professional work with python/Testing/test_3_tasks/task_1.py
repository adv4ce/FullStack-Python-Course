def check_triangle(side1: int, side2: int, side3: int) -> str:
    if side1 + side2 < side3 or side2 + side3 < side1 or side3 + side1 < side2:
        result = "Треугольник не существует"
    elif side1 == side2 == side3:
        result = "Равносторонний треугольник"
    elif (
        ((side1 == side2) and (side1 != side3))
        or ((side2 == side3) and (side2 != side1))
        or ((side1 == side3) and (side1 != side2))
    ):
        result = "Равнобедренный треугольник"
    else:
        result = "Разносторонний треугольник"
    return result
