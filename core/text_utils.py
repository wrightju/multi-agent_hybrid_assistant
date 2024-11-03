import tiktoken

def chunk_text(text, max_tokens=1000):
    """
    Splits a text into chunks, each within the max token limit.
    
    Parameters:
    - text (str): The text to split.
    - max_tokens (int): The maximum tokens per chunk.
    
    Returns:
    - list of str: List of text chunks.
    """
    encoding = tiktoken.encoding_for_model("text-embedding-ada-002")
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(encoding.encode(" ".join(current_chunk))) > max_tokens:
            chunks.append(" ".join(current_chunk[:-1]))  # Exclude the last word to stay within limit
            current_chunk = [word]
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
