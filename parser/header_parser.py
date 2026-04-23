def normalize_headers(headers):
    return {k.strip(): v.strip() for k, v in headers.items()}
