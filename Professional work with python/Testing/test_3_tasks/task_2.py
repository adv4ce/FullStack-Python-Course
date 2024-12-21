def discriminant(a, b, c):
    return pow(b, 2) - (4 * a * c)


def solution(a, b, c):
    d = discriminant(a, b, c)
    if d > 0:
        return [(-b + d**0.5) / (a * 2), (-b - d**0.5) / (a * 2)]
    elif d == 0:
        return [-b / (a * 2)]
    else:
        return ["корней нет"]
