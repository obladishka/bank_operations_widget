from datetime import datetime


def log(filename=None):
    """Decorator for logging function start and end time, execution result and errors information."""

    def my_decorator(func):
        def wrapper(*args, **kwargs):

            start_time = datetime.now()

            try:
                func(*args, **kwargs)
            except Exception as e:
                log_message = f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}"
            else:
                log_message = f"{func.__name__} ok"

            end_time = datetime.now()

            if filename:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(f"{func.__name__} start time: {start_time} ")
                    file.write(log_message)
                    file.write(f" {func.__name__} end time: {end_time}")
            else:
                print(f"{func.__name__} start time: {start_time}")
                print(log_message)
                print(f"{func.__name__} end time: {end_time}")

        return wrapper

    return my_decorator
