"""General utility functions."""

def format_file_size(bytes_size: int) -> str:
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 ** 2:
        return f"{bytes_size / 1024:.1f} KB"
    else:
        return f"{bytes_size / (1024 ** 2):.1f} MB"
