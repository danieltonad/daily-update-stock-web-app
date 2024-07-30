def split_list(data: list, size: int):
    return [data[i:i + size] for i in range(0, len(data), size)]