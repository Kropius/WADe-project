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
text_content = "Update the cat that has id 6 with black fur"
document = {"content": text_content, "type_": text_type, "language": language}
encoding_type = language_v1.EncodingType.UTF8
response = language_client.analyze_syntax(request={'document': document, 'encoding_type': encoding_type})
# print(response)

get_synonyms = ['get', 'retrieve', 'acquire', 'obtain', 'read', 'show', 'view']
post_synonyms = ['create', 'insert', 'add', 'append', 'write']
put_synonyms = ['replace']
patch_synonyms = ['update', 'improve']
delete_synonyms = ['remove', 'delete', 'kill', 'reduce']


def append_lists_lambda(x, y):
    return x + y


get_verb_representatives = reduce(append_lists_lambda, [wordnet.synsets(word) for word in get_synonyms])
post_verb_representatives = reduce(append_lists_lambda, [wordnet.synsets(word) for word in post_synonyms])
put_verb_representatives = reduce(append_lists_lambda, [wordnet.synsets(word) for word in put_synonyms])
patch_verb_representatives = reduce(append_lists_lambda, [wordnet.synsets(word) for word in patch_synonyms])
delete_verb_representatives = reduce(append_lists_lambda, [wordnet.synsets(word) for word in delete_synonyms])


def find_http_verb(nlp_response):
    verb_list = []
    for index, token in enumerate(nlp_response.tokens):
        if token.part_of_speech.tag.name == 'VERB':
            verb_list.append((index, token.text.content))

    max_similarity = 0
    content_verb = verb_list[0]
    http_verb = 'GET'

    for candidate_verb in verb_list:
        candidate_verb_representatives = wordnet.synsets(candidate_verb[1])

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

    return content_verb, http_verb


def find_main_entity(nlp_response, valid_entities, http_verb_index):
    entity_list = []
    for index, token in enumerate(nlp_response.tokens):
        if token.dependency_edge.label.name == 'ROOT':
            continue
        if token.dependency_edge.head_token_index == http_verb_index and token.part_of_speech.tag.name == 'NOUN':
            entity_list.append((index, token.text.content))

    max_similarity = 0
    entity_correspondent = entity_list[0]
    real_entity_name = valid_entities[0]

    for entity in entity_list:
        candidate_entity_synset = wordnet.synsets(entity[1])[0]
        for valid_entity in valid_entities:
            valid_entity_synset = wordnet.synsets(valid_entity)[0]
            current_similarity = candidate_entity_synset.wup_similarity(valid_entity_synset)
            if current_similarity > max_similarity:
                max_similarity = current_similarity
                entity_correspondent = entity
                real_entity_name = valid_entity

    if max_similarity < 0.5:
        raise Exception('Unfortunatelly, no entity matched your input!')
    return entity_correspondent, real_entity_name


def recursive_find_noun_attributes(nlp_response, dependency_index):
    noun_attributes = []
    for index, token in enumerate(nlp_response.tokens):
        if token.dependency_edge.head_token_index == dependency_index:
            if token.part_of_speech.tag.name == 'NOUN':
                noun_attributes.append((index, token.text.content))
            noun_attributes = noun_attributes + recursive_find_noun_attributes(nlp_response, index)
    return noun_attributes


def find_attribute_names(nlp_response, valid_attributes, entity_index):
    real_attribute_list = []
    values_list = []
    for index, token in enumerate(nlp_response.tokens):
        if token.dependency_edge.head_token_index == entity_index and token.part_of_speech.tag.name == 'ADJ':
            values_list.append((index, token.text.content))

    sentence_attributes = values_list + recursive_find_noun_attributes(nlp_response, entity_index)

    for attribute in sentence_attributes:
        attribute_synsets = wordnet.synsets(attribute[1])
        max_similarity = 0
        real_attribute_name = valid_attributes[0]
        for valid_attribute in valid_attributes:
            valid_attribute_synsets = wordnet.synsets(valid_attribute)
            for attribute_synset in attribute_synsets:
                for valid_attribute_synset in valid_attribute_synsets:
                    current_similarity = attribute_synset.wup_similarity(valid_attribute_synset)
                    if current_similarity > max_similarity:
                        max_similarity = current_similarity
                        real_attribute_name = valid_attribute
        real_attribute_list.append(real_attribute_name)

    return sentence_attributes, real_attribute_list, values_list


def find_rest_of_attribute_values(nlp_response, sentence_attributes, found_values):
    unmapped_attributes = sentence_attributes[len(found_values):]
    all_values = found_values
    for attribute in unmapped_attributes:
        for index, token in enumerate(nlp_response.tokens):
            if token.dependency_edge.head_token_index == attribute[0] and \
                    (token.part_of_speech.tag.name == 'ADJ' or token.part_of_speech.tag.name == 'NUM'):
                all_values.append((index, token.text.content))
    return all_values


def get_final_result(verb, entity, attribute_names, values):
    path = '/' + entity
    query_params = '?'
    for index, attribute in enumerate(attribute_names):
        query_params += attribute + '=' + values[index][1] + '&'
    query_params = query_params[:-1]
    return verb + ' on ' + path + query_params


entities = ['feline', 'weapon', 'human', 'store']
attributes = ['feeling', 'color', 'muscle', 'id', 'members', 'gender']

print('Main Sentence: ' + text_content)
print('\nMatched HTTP Verb: ')
matched_verb = find_http_verb(response)
print(matched_verb)
print('\nFrom entity list: ' + str(entities) + ', I Matched Entity: ')
main_entity = find_main_entity(response, entities, matched_verb[0][0])
print(main_entity)
print('\nFrom attribute list: ' + str(attributes), ', I matched attributes: ')
attribute_search_result = find_attribute_names(response, attributes, main_entity[0][0])
print(attribute_search_result)
print('\nAttribute values: ')
all_attribute_values = find_rest_of_attribute_values(response, attribute_search_result[0], attribute_search_result[2])
print(all_attribute_values)
print('\n')
print(get_final_result(matched_verb[1], main_entity[1], attribute_search_result[1], all_attribute_values))
