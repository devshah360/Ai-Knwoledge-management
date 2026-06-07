def calculate_score(
    elastic_score,
    vector_rank
):

    return (
        elastic_score * 0.7
    ) + (
        vector_rank * 0.3
    )