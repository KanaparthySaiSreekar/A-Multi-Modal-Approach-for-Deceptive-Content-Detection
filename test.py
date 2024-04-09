from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define the sentences
sentence1 = "IPL 2023 Final: Chennai Super Kings crowned IPL champions for 5th time after thrilling win over Gujarat Titans"
sentence2 = "CSK vs GT, IPL 2023: Here are the top moments and highlights from the thrilling final between Chennai Super Kings and Gujarat Titans on Tuesday."

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the sentences
tfidf_matrix = vectorizer.fit_transform([sentence1, sentence2])

# Compute cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

print("Cosine Similarity:", cosine_sim[0][0])
