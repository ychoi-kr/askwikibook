def contains_any(query, keywords):
    return any(keyword in query for keyword in keywords)
