import nltk
import os

def get_entities(text):
    try:
        os.environ[os.environ.get('cert_file_default')] = os.environ.get('cert_file_name')
        nltk.download('maxent_ne_chunker')
        tokens = nltk.word_tokenize(text)
        tagged_tokens = nltk.pos_tag(tokens)
        ne_tree = nltk.ne_chunk(tagged_tokens)
        entities = []
        organizations = []
        gpe = []
        locations = []
        others = []

        for subtree in ne_tree.subtrees():
            if subtree.label() == 'PERSON':
                entities.append(' '.join([token for token, pos in subtree.leaves()]))
            elif subtree.label() == 'ORGANIZATION':
                organizations.append(' '.join([token for token, pos in subtree.leaves()]))
            elif subtree.label() == 'GPE':
                gpe.append(' '.join([token for token, pos in subtree.leaves()]))
            elif subtree.label() == 'LOCATION':
                locations.append(' '.join([token for token, pos in subtree.leaves()]))
            else:
                others.append(' '.join([token for token, pos in subtree.leaves()]))

        # Convert entities to a delimiter-separated string
        entities_csv = ":::".join(entities)
        organizations_csv = ":::".join(organizations)
        gpe_csv = ":::".join(gpe)
        locations_csv = ":::".join(locations)
        others_csv = ":::".join(others)

        # Make the entities, organizations, gpe, locations and others as a dictionary
        entities_dict = {
            "Entities": entities_csv,
            "Organizations": organizations_csv,
            "Gpe": gpe_csv,
            "Locations": locations_csv,
            "Others": others_csv
        }
        return entities_dict
    except Exception as e:
        print(f"Error in get_entities: {e}")
        return {"entities": ""}