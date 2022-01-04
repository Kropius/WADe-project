import os
from google.cloud import language_v1
from nltk.corpus import wordnet

# import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'avid-airway-337117-d28d91542407.json'
language_client = language_v1.LanguageServiceClient()
text_type = language_v1.Document.Type.PLAIN_TEXT

language = "en"
text_content = "Show me all cats with blue colouring."
document = {"content": text_content, "type_": text_type, "language": language}

encoding_type = language_v1.EncodingType.UTF8

response = language_client.analyze_syntax(request={'document': document, 'encoding_type': encoding_type})

verb = "show"
syns = wordnet.synsets(verb)
print(syns[0])

print(response)
