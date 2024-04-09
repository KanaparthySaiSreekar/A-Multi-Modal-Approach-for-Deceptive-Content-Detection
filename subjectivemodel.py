import json
import requests
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
class subjective:
    def __init__(self):
        self.headers = {"Authorization": "Bearer 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"}
        self.API_URL = "https://api-inference.huggingface.co/models/lighteternal/fact-or-opinion-xlmr-el"
        self.model_name = "lighteternal/fact-or-opinion-xlmr-el"
        self.model = AutoModelForSequenceClassification.from_pretrained('lighteternal')
        self.tokenizer = AutoTokenizer.from_pretrained('lighteternal')
    def api_request(self, text):
        data = self.query({"text": text})
        print(data)
        data1, label = data[0]['score'], data[0]['label']
        if label == 'LABEL_0':
            return "subjective"
        else:
            return "objective"

    def query(self, payload):
        send_data = json.dumps(payload)
        response = requests.request("POST", self.API_URL, headers=self.headers, data=send_data)
        return json.loads(response.content.decode("utf-8"))

    def send_request(self, text):
        inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')

        with torch.no_grad():
            outputs = self.model(**inputs)

        predicted_label = torch.argmax(outputs.logits).item()
        print(predicted_label)

        if predicted_label == 0:
            return "subjective"

        else:
            return "objective"

# print(subjective().send_request('i play football'))

# from transformers import MarianTokenizer, MarianMTModel
#
# # Load the pretrained MarianMT model and tokenizer for English to Hindi translation
# model_name = "Helsinki-NLP/opus-mt-en-hi"
# tokenizer = MarianTokenizer.from_pretrained(model_name)
# model = MarianMTModel.from_pretrained(model_name)
#
# # English text to be translated
# english_text = "Hello, how are you?"
#
# # Tokenize and translate the English text to Hindi
# inputs = tokenizer.encode(english_text, return_tensors="pt")
# translated_ids = model.generate(inputs, max_length=50, num_beams=4, length_penalty=2.0, early_stopping=True)
# translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
#
# print("English: ", english_text)
# print("Hindi: ", translated_text)