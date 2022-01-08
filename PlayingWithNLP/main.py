import os
from google.cloud import language_v1
from nltk.corpus import wordnet
from functools import reduce

# import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'avid-airway-337117-d28d91542407.json'
language_client = language_v1.LanguageServiceClient()
text_type = language_v1.Document.Type.PLAIN_TEXT

language = "en"
text_content = "i want to visualise all gluten-free products"
document = {"content": text_content, "type_": text_type, "language": language}

get_synonyms = ['get', 'retrieve', 'acquire', 'obtain', 'read', 'show', 'view']
post_synonyms = ['create', 'insert', 'add', 'append', 'write']
put_synonyms = ['replace', 'change']
patch_synonyms = ['update', 'improve']
delete_synonyms = ['remove', 'delete', 'kill', 'reduce']


def append_lists_lambda(x, y):
    return x + y


get_verb_representatives = reduce(append_lists_lambda, [wordnet.synsets(word) for word in get_synonyms])
post_verb_representatives = reduce(append_lists_lambda, [wordnet.synsets(word) for word in post_synonyms])
put_verb_representatives = reduce(append_lists_lambda, [wordnet.synsets(word) for word in put_synonyms])
patch_verb_representatives = reduce(append_lists_lambda, [wordnet.synsets(word) for word in patch_synonyms])
delete_verb_representatives = reduce(append_lists_lambda, [wordnet.synsets(word) for word in delete_synonyms])


encoding_type = language_v1.EncodingType.UTF8

response = language_client.analyze_syntax(request={'document': document, 'encoding_type': encoding_type})


def find_http_verb(nlp_response):
    verb_list = []
    for token in nlp_response.tokens:
        if token.part_of_speech.tag.name == 'VERB':
            verb_list.append(token.text.content)

    max_similarity = 0
    content_verb = verb_list[0]
    http_verb = 'GET'

    for candidate_verb in verb_list:
        candidate_verb_representatives = wordnet.synsets(candidate_verb)

        for candidate_verb_representative in candidate_verb_representatives:
            for get_verb_representative in get_verb_representatives:
                current_max_similarity = get_verb_representative.wup_similarity(candidate_verb_representative)
                if max_similarity < current_max_similarity:
                    max_similarity = current_max_similarity
                    content_verb = candidate_verb
                    http_verb = 'GET'

            for post_verb_representative in post_verb_representatives:
                current_max_similarity = post_verb_representative.wup_similarity(candidate_verb_representative)
                if max_similarity < current_max_similarity:
                    max_similarity = current_max_similarity
                    content_verb = candidate_verb
                    http_verb = 'POST'

            for put_verb_representative in put_verb_representatives:
                current_max_similarity = put_verb_representative.wup_similarity(candidate_verb_representative)
                if max_similarity < current_max_similarity:
                    max_similarity = current_max_similarity
                    content_verb = candidate_verb
                    http_verb = 'PUT'

            for patch_verb_representative in patch_verb_representatives:
                current_max_similarity = patch_verb_representative.wup_similarity(candidate_verb_representative)
                if max_similarity < current_max_similarity:
                    max_similarity = current_max_similarity
                    content_verb = candidate_verb
                    http_verb = 'PATCH'

            for delete_verb_representative in delete_verb_representatives:
                current_max_similarity = delete_verb_representative.wup_similarity(candidate_verb_representative)
                if max_similarity < current_max_similarity:
                    max_similarity = current_max_similarity
                    content_verb = candidate_verb
                    http_verb = 'DELETE'

    print(max_similarity)
    return content_verb, http_verb


print(find_http_verb(response))
