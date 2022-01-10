import utils.costants as label


def get_sentiment_by_scores(scores):
    max_rank = max(scores)
    sentiment_index = scores.index(max_rank)

    if sentiment_index == 0:
        return label.NEGATIVE
    elif sentiment_index == 1:
        return label.NEUTRAL
    elif sentiment_index == 2:
        return label.POSITIVE
