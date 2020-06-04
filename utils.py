def calculate_words_per_minute(text, time, sep='_'):
    words_in_text = len(text.split(sep))
    words_per_minute = int(round(words_in_text / time * 60))
    return words_per_minute
