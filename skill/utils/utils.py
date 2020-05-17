def get_tokens(alice_request):
    return " ".join(alice_request.request.nlu.tokens).replace("ё", "е").lower()


def get_original_utterance(alice_request):
    return alice_request.request.command.replace("ё", "е")
