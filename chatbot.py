import time
import numpy as np
import anthropic

anthropic.api_key = "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"


class chatBot:
    def __init__(self):
        self.received_answer = ""
        self.received_question = ""

    def get_anthropic_embedding(self, text):
        self.received_question = text
        resp = anthropic.embeddings(
            text,
            model="claude-v1-embeddings",
            max_tokens=128,
            n=1,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return resp.embeddings[0]

    def get_answer(self, user_question):
        user_question_embedding = self.get_anthropic_embedding(user_question)
        similarity_scores = np.dot(questions_embeddings, user_question_embedding)
        most_similar_index = np.argmax(similarity_scores)
        print(np.max(similarity_scores))
        if np.max(similarity_scores) < 0.8:
            self.received_answer = "I am sorry! could you please rephrase the question"
        else:
            most_similar_question = questions[most_similar_index]
            supported_answer = answers[most_similar_index]
            self.received_answer = supported_answer
        return self.received_answer
