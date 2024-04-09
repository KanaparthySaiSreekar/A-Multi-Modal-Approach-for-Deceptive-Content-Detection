from transformers import AutoModelForTokenClassification, AutoTokenizer

model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
model = AutoModelForTokenClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save the model and tokenizer
model.save_pretrained("dbmbz")
tokenizer.save_pretrained("dbmbz")
