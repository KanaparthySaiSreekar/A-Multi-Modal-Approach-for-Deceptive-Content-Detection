import time

from transformers import BertModel, BertTokenizer
import time

from questionanswer import questions, answers
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model_path = "C:/Users/vixha/Downloads/bert"
tim = time.time()
model1 = BertModel.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)
model = SentenceTransformer(modules=[model1])
print(time.time()-tim)

document_embeddings = model.encode(questions)
query_embedding = model.encode(["explain me about newstitle check"])
similarities = cosine_similarity(query_embedding, document_embeddings)[0]
max_similarity_index = similarities.argmax()
most_similar_document = questions[max_similarity_index]
similarity_score = similarities[max_similarity_index]
print(answers[max_similarity_index])

from sentence_transformers import SentenceTransformer
modelPath = "C:/Users/vixha/Downloads/bert"
tim = time.time()
model = SentenceTransformer(modelPath)
print(time.time()-tim)
query_embedding = model.encode(["explain me about newstitle check"])
document_embeddings = model.encode(questions)

similarities = cosine_similarity(query_embedding, document_embeddings)[0]
max_similarity_index = similarities.argmax()
most_similar_document = questions[max_similarity_index]
similarity_score = similarities[max_similarity_index]

print(answers[max_similarity_index])