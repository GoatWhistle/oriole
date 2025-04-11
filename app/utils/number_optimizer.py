def get_number_one_bit_less(n: int) -> int:
    power_of_two = 1
    while power_of_two <= n:
        power_of_two *= 2
    return power_of_two - 1
