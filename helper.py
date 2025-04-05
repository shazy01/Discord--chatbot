def split_text_into_chunks(text, max_length=2000):
    start = 0
    text_length = len(text)
    chunks = []

    while start < text_length:
        end = min(start + max_length, text_length)

        # If we're at the end of the text, take the rest
        if end == text_length:
            chunks.append(text[start:end])
            break

        # Find the last space within the current chunk
        last_space_index = text.rfind(' ', start, end)

        if last_space_index != -1:
            # Split at the last space within the limit
            chunks.append(text[start:last_space_index])
            start = last_space_index + 1
        else:
            # No spaces found, split at max_length
            chunks.append(text[start:end])
            start = end

    return chunks
