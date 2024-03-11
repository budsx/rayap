def build_query_string(query):
    # Sanity check
    if not query or not isinstance(query, dict) or len(query) == 0:
        return ''
    # Build and return query string
    return '&'.join([f"{key}={query[key]}" for key in query])