import time
from functools import wraps


def timeMethod(func):
    # runs timer on wrapped function
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            funcName = f"{func.__qualname__}()"
        except:
            funcName = "unknownMethod"
        print(f">> Starting function: {funcName}\n")
        startTime = time.time()
        ret = func(*args, **kwargs)
        endTime = time.time()
        print(f"<< Ending function: {funcName}")
        print(f"--- Function {funcName} ran in {str(endTime - startTime).split('.')[0]} seconds ---\n")
        return ret

    return wrapper
