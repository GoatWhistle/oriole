def camel_case_to_snake_case(camel: str) -> str:
    snake = []
    for index, char in enumerate(camel):
        if index and char.isupper():
            next_index = index + 1
            flag = next_index >= len(camel) or camel[next_index].isupper()
            prev_char = camel[index - 1]
            if not (prev_char.isupper() and flag):
                snake.append("_")
        snake.append(char.lower())
    return "".join(snake)
