import os
import json
from google.cloud import language_v1
from nltk.corpus import wordnet
from functools import reduce
import functions_framework
import constants
import requests
import nltk.data


def initialize_data(text_content, api_spec_id, text_type, language_client):
    nlp_response = get_new_nlp_response(text_content, text_type, language_client)

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

    api_spec_response = requests.get(constants.GET_SPEC_URL + str(api_spec_id) + '?key=' + constants.API_KEY)
    api_spec_response_dict = api_spec_response.json()

    api_spec_data = {
        'allowed_operations': api_spec_response_dict['allowed_operations'],
        'allowed_attributes': api_spec_response_dict['allowed_attributes']
    }

    for entity, attribute_list in api_spec_data['allowed_attributes'].items():
        api_spec_data['allowed_attributes'][entity] = list(set([list(attribute.keys())[0] for attribute in attribute_list]))

    print(api_spec_data)

    return nlp_response, get_verb_representatives, post_verb_representatives, put_verb_representatives, \
        patch_verb_representatives, delete_verb_representatives, api_spec_data


def get_new_nlp_response(text_content, text_type, language_client):
    language = "en"
    if text_content[-1] not in ['.', '!', '?']:
        text_content += '.'
    document = {"content": text_content, "type_": text_type, "language": language}
    encoding_type = language_v1.EncodingType.UTF8
    response = language_client.analyze_syntax(request={'document': document, 'encoding_type': encoding_type})
    return response


def find_http_verb(nlp_response, get_verb_representatives, post_verb_representatives,
                   put_verb_representatives, patch_verb_representatives, delete_verb_representatives):
    verb_list = []
    for index, token in enumerate(nlp_response.tokens):
        if token.part_of_speech.tag.name == 'VERB':
            verb_list.append((index, token.text.content))

    if len(verb_list) == 0:
        return '', ''

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

    if max_similarity == 0:
        return '', ''

    return content_verb, http_verb


def find_main_entity(nlp_response, valid_entities, http_verb_index):
    error_entity_not_amongst_valid_ones = False
    entity_list = []
    for index, token in enumerate(nlp_response.tokens):
        if token.dependency_edge.label.name == 'ROOT':
            continue
        if token.dependency_edge.head_token_index == http_verb_index and token.part_of_speech.tag.name == 'NOUN':
            entity_list.append((index, token.text.content))

    if len(entity_list) == 0:
        return ('', ''), error_entity_not_amongst_valid_ones

    max_similarity = 0
    entity_correspondent = entity_list[0]
    real_entity_name = valid_entities[0]

    for entity in entity_list:
        candidate_entity_synset = wordnet.synsets(entity[1])[0] if len(wordnet.synsets(entity[1])) > 0 else None
        if candidate_entity_synset is None:
            continue
        for valid_entity in valid_entities:
            valid_entity_synset = wordnet.synsets(valid_entity)[0]
            current_similarity = candidate_entity_synset.wup_similarity(valid_entity_synset)
            if current_similarity > max_similarity:
                max_similarity = current_similarity
                entity_correspondent = entity
                real_entity_name = valid_entity

    if max_similarity < 0.6:
        error_entity_not_amongst_valid_ones = True
    return (entity_correspondent, real_entity_name), error_entity_not_amongst_valid_ones


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
    response_dict = dict()
    path = '/' + entity
    response_dict['verb'] = verb
    response_dict['path'] = path
    if verb in ['GET', 'DELETE']:
        query_params = '?'
        for index, attribute in enumerate(attribute_names):
            query_params += attribute + '=' + values[index][1] + '&'
        query_params = query_params[:-1]
        response_dict['query_params'] = query_params
    else:
        request_body = dict()
        for index, attribute in enumerate(attribute_names):
            request_body[attribute] = values[index][1]
        response_dict['request_body'] = request_body

    return response_dict


def post(request):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print('Root dir: ' + root_dir)
    nltk_dir = os.path.join(root_dir, 'nltk_data')
    nltk.data.path.append(nltk_dir)

    response_headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    language_client = language_v1.LanguageServiceClient()
    text_type = language_v1.Document.Type.PLAIN_TEXT

    request_json = request.get_json()
    if request_json and 'text_content' in request_json:
        print('From function: ' + request_json['text_content'])
        text_content = request_json['text_content']
    else:
        error_response_body = {
            'message': 'text_content attribute is missing from your request body!'
        }
        return error_response_body, 400, response_headers
    if request.args and request.args.get('id'):
        print('From function: ' + str(request.args.get('id')))
        api_spec_id = request.args.get('id')
    else:
        error_response_body = {
            'message': 'The API Specification ID is missing from the path params!'
        }
        return error_response_body, 400, response_headers

    response, get_verb_repr, post_verb_repr, put_verb_repr, \
        patch_verb_repr, delete_verb_repr, parsed_api_spec = initialize_data(text_content, api_spec_id, text_type, language_client)

    print('Main Sentence: ' + text_content)

    print('\nMatched HTTP Verb: ')
    matched_verb = find_http_verb(response, get_verb_repr, post_verb_repr,
                                  put_verb_repr, patch_verb_repr, delete_verb_repr)
    print(matched_verb)
    if matched_verb == ('', ''):
        error_response_body = {
            'message': 'Please provide at least one valid VERB in your sentence!'
        }
        return error_response_body, 412, response_headers

    if matched_verb[1] == 'GET' and 'with' in text_content:
        text_content = text_content.replace('with', 'having')
        response = get_new_nlp_response(text_content, text_type, language_client)

    supported_entities_for_found_verb = parsed_api_spec['allowed_operations'][matched_verb[1]]
    print('\nFrom entity list: ' + str(supported_entities_for_found_verb) + ', I matched entity: ')
    main_entity_search_result = find_main_entity(response, supported_entities_for_found_verb, matched_verb[0][0])
    main_entity = main_entity_search_result[0]
    error_finding_entity = main_entity_search_result[1]
    if error_finding_entity:
        error_response_body = {
            'message': 'The highest similarity between the provided entity ' + main_entity[0][1].upper() +
                       ' and any of the supported API entities is too small OR the matched verb ' +
                       matched_verb[1] + ' does not operate with the entity: ' + main_entity[0][1].upper() + '!'
        }
        return error_response_body, 412, response_headers
    print(main_entity)
    if main_entity == ('', ''):
        error_response_body = {
            'message': 'Please provide at least one valid NOUN in your sentence!'
        }
        return error_response_body, 412, response_headers

    supported_attributes_for_found_entity = parsed_api_spec['allowed_attributes'][main_entity[1]]
    print('\nFrom attribute list: ' + str(supported_attributes_for_found_entity), ', I matched attributes: ')
    attribute_search_result = find_attribute_names(response, supported_attributes_for_found_entity, main_entity[0][0])
    for index, elem in enumerate(attribute_search_result[0]):
        if elem[1] == main_entity[0][1]:
            del attribute_search_result[0][index]
            del attribute_search_result[1][index]
    print(attribute_search_result)

    print('\nAttribute values: ')
    all_attribute_values = find_rest_of_attribute_values(response, attribute_search_result[0], attribute_search_result[2])
    print(all_attribute_values)

    final_result = get_final_result(matched_verb[1], main_entity[1], attribute_search_result[1], all_attribute_values)
    print('\n')
    print(final_result)

    return final_result, 200, response_headers


def options(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    return '', 204, headers


@functions_framework.errorhandler(NotImplementedError)
def handle_405(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({
        "message": "Method not allowed",
        "code": 405
    }), 405, headers


@functions_framework.errorhandler(Exception)
def handle_500(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({
        "message": "Something went wrong. Please try again...",
        "code": 500
    }), 500, headers


@functions_framework.http
def nlp_to_rest(request):
    if request.method == 'OPTIONS':
        return options(request)
    if request.method == 'POST':
        return post(request)
    raise NotImplementedError()
