import time


# Function to convert milliseconds to a readable duration
def millis_to_duration(ms):
    seconds = ms // 1000

    formatted_time = time.strftime('%M:%S', time.gmtime(seconds))

    return f'{formatted_time}'
