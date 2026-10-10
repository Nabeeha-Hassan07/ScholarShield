from nlp.syntax import analyze_syntax


def extract_predicates(text):
    """
    Extract verbs that act as predicates.
    """
    if not text:
        return []

    syntax_result = analyze_syntax(text)
    predicates = []

    for sentence in syntax_result["sentences"]:
        for token in sentence["tokens"]:
            if token["pos"] == "VERB":
                predicates.append({
                    "predicate": token["lemma"],
                    "text": token["text"],
                    "pos": token["pos"],
                    "dependency": token["dependency"]
                })

    return predicates


def get_child_tokens(sentence_tokens, head_text):
    """
    Return tokens whose syntactic head is the given word.
    """
    return [
        token
        for token in sentence_tokens
        if token["head"] == head_text
    ]


def collect_phrase(sentence_tokens, root_text):
    """
    Collect all dependency-connected words belonging to a phrase.

    The returned phrase already contains the root token, so callers
    must NOT append the root token again.
    """

    if not sentence_tokens or not root_text:
        return []

    root_text = str(root_text).strip()

    root_token = None

    for token in sentence_tokens:

        token_text = str(
            token.get("text", "")
        ).strip()

        if token_text.lower() == root_text.lower():

            root_token = token
            break

    if root_token is None:
        return []

    children = {}

    for token in sentence_tokens:

        token_id = token.get("id")
        head_id = token.get("head")

        if token_id is None or head_id is None:
            continue

        children.setdefault(
            head_id,
            []
        ).append(token)

    visited = set()
    collected = []

    def visit(token):

        token_id = token.get("id")

        if token_id in visited:
            return

        visited.add(token_id)

        token_text = str(
            token.get("text", "")
        ).strip()

        if token_text:
            collected.append(
                {
                    "id": token_id,
                    "text": token_text
                }
            )

        for child in children.get(
            token_id,
            []
        ):

            visit(child)

    visit(root_token)

    collected.sort(
        key=lambda item: (
            item["id"]
            if isinstance(
                item["id"],
                (int, float)
            )
            else 0
        )
    )

    return [
        item["text"]
        for item in collected
    ]


def extract_arguments(sentence_tokens, predicate_token):
    """
    Extract predicate-argument information.

    Phrase extraction already includes the dependency-root token,
    so subject/object phrases are not duplicated.
    """

    subject = []
    direct_object = []
    indirect_object = []
    modifiers = []
    negation = []

    predicate_text = predicate_token["text"]

    children = get_child_tokens(
        sentence_tokens,
        predicate_text
    )

    for token in children:

        dependency = token["dependency"]

        if dependency in {
            "nsubj",
            "nsubjpass",
            "csubj"
        }:

            phrase = collect_phrase(
                sentence_tokens,
                token["text"]
            )

            if phrase:
                subject.append(
                    " ".join(phrase)
                )

        elif dependency in {
            "dobj",
            "obj"
        }:

            phrase = collect_phrase(
                sentence_tokens,
                token["text"]
            )

            if phrase:
                direct_object.append(
                    " ".join(phrase)
                )

        elif dependency == "iobj":

            phrase = collect_phrase(
                sentence_tokens,
                token["text"]
            )

            if phrase:
                indirect_object.append(
                    " ".join(phrase)
                )

        elif dependency in {
            "advmod",
            "obl",
            "npadvmod"
        }:

            phrase = collect_phrase(
                sentence_tokens,
                token["text"]
            )

            if phrase:
                modifiers.append(
                    " ".join(phrase)
                )

        elif dependency == "neg":

            negation.append(
                token["text"]
            )

    return {
        "subject": subject,
        "object": direct_object,
        "indirect_object": indirect_object,
        "modifiers": modifiers,
        "negation": negation
    }


def inherit_subject(
    frames,
    current_arguments
):
    """
    Handle predicates such as:

    Researchers analyze data to identify patterns.

    The subject of 'identify' is inherited
    from the previous predicate.
    """

    if current_arguments["subject"]:
        return current_arguments

    if not frames:
        return current_arguments

    previous_subject = frames[-1]["arguments"]["subject"]

    if previous_subject:
        current_arguments["subject"] = previous_subject.copy()

    return current_arguments


def extract_semantic_frames(text):
    """
    Build predicate-argument frames for each sentence.
    """

    if not text:
        return []

    syntax_result = analyze_syntax(text)
    frames = []

    for sentence in syntax_result["sentences"]:

        sentence_tokens = sentence["tokens"]

        # Reset inherited subject at sentence boundaries.
        sentence_frames = []

        for predicate_token in sentence_tokens:

            if predicate_token["pos"] != "VERB":
                continue

            arguments = extract_arguments(
                sentence_tokens,
                predicate_token
            )

            # Inherit only from a predicate in the SAME sentence.
            if not arguments["subject"] and sentence_frames:
                previous_subject = sentence_frames[-1]["arguments"]["subject"]

                if previous_subject:
                    arguments["subject"] = previous_subject.copy()

            frame = {
                "sentence": sentence["text"],
                "predicate": predicate_token["lemma"],
                "predicate_text": predicate_token["text"],
                "arguments": arguments
            }

            sentence_frames.append(frame)
            frames.append(frame)

    return frames


def meaning_representation(text):
    """
    Generate the complete meaning representation.
    """

    if not text:
        return {
            "predicates": [],
            "semantic_frames": []
        }

    predicates = extract_predicates(text)
    semantic_frames = extract_semantic_frames(text)

    return {
        "predicates": predicates,
        "semantic_frames": semantic_frames
    }
