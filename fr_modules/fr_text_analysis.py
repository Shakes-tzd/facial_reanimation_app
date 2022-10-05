import spacy
def process_text(doc):
    tokens = []
    for token in doc:

        if (token.ent_type_ == "CARDINAL") or token.like_num:
            tokens.append((token.text, "", "#faa"))
        # else:
        #     if (token.text == "patients") or (token.text == "patient") or (token.text == "case") or (token.text == "cases"):
        #         tokens.append((token.text, "", "#00968C"))
        #     else:
        #         if (token.text == "double") or (token.text == "dual"):
        #             tokens.append((token.text, "", "#8ef"))
        else:
            tokens.append(" " + token.text + " ")
    return tokens

def load_models():
    # french_model = spacy.load("models/fr/")
    english_model = spacy.load("models/en")
    models = {"en": english_model}  # , "fr": french_model}
    return models

def resamble(plain_text, entities):
    ll = []
    entities_copy = entities.copy()
    prev_ent_idx = 0
    current_ent_idx = 0
    while len(entities) > 0:
        if len(ll) == 0:
            ll.append(plain_text[:entities[current_ent_idx]["start"]])
            ll.append((plain_text[entities[0]["start"]:entities[0]["end"]],
                      entities[0]["label"], ent_color_mapping[entities[0]["label"]]))
        else:
            ll.append(
                plain_text[entities_copy[prev_ent_idx-1]["end"]:entities[0]["start"]])
            ll.append((plain_text[entities[0]["start"]:entities[0]["end"]],
                      entities[0]["label"], ent_color_mapping[entities[0]["label"]]))
        if len(entities) > 1:
            del entities[0]
            prev_ent_idx += 1
            continue
        else:
            ll.append(plain_text[entities[0]["end"]:])
            del entities[0]
    return ll

def map_entities(doc):
    plain_text = doc.text
    entities = text.entities
    return resamble(plain_text, entities)