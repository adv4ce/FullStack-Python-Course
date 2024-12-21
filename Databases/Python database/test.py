def find_next_square(sq):
    sqrt = sq ** 0.5
    if sqrt == int(sqrt):
        return (int(sqrt) + 1) ** 2
    return -1


print(find_next_square(120))
