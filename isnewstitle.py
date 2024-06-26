import nltk
import string as s
import pandas as pd
import pickle
import joblib


class checkNewsTitle:
    def __init__(self, title):
        self.result = 0
        self.headline = title
        self.lemmatize = nltk.stem.WordNetLemmatizer()

    def tokenization(self, text):
        lst = text.split()
        return lst

    def lowercasing(self, lst):
        new_lst = []
        for i in lst:
            new_lst.append(i.lower())
        return new_lst

    def remove_punctuations(self, lst):
        new_lst = []
        for i in lst:
            for j in s.punctuation:
                i = i.replace(j, '')
            new_lst.append(i)
        return new_lst

    def remove_numbers(self, lst):
        nodig_lst = []
        new_lst = []
        for i in lst:
            for j in s.digits:
                i = i.replace(j, '')
            nodig_lst.append(i)
        for i in nodig_lst:
            if i != '':
                new_lst.append(i)
        return new_lst

    def remove_spaces(self, lst):
        new_lst = []
        for i in lst:
            i = i.strip()
            new_lst.append(i)
        return new_lst

    def lemmatzation(self, lst):
        new_lst = []
        for i in lst:
            i = self.lemmatize.lemmatize(i)
            new_lst.append(i)
        return new_lst

    def vectorize(self, lst):
        dg = ''
        for i in lst:
            dg += i
            dg += ' '
        with open("vectorizers/wevec.pkl", 'rb') as fin:
            tfidf = pickle.load(fin)
            return tfidf.transform(pd.Series({1: dg}))

    def predict(self, lst):
        with open("mlmodels/wewill.pkl", 'rb') as ld:
            model = joblib.load(ld)
            return model.predict(lst)

    def run(self):
        self.headline = self.tokenization(self.headline)
        self.headline = self.lowercasing(self.headline)
        self.headline = self.remove_spaces(self.headline)
        self.headline = self.remove_numbers(self.headline)
        self.headline = self.remove_punctuations(self.headline)
        self.headline = self.lemmatzation(self.headline)
        self.headline = self.vectorize(self.headline)
        self.result = self.predict(self.headline)
        return self.result

# print(checkNewsTitle('The 26 parties at the Opposition meeting announced the name of their alliance — INDIA, standing for Indian National Developmental, Inclusive Alliance').run())



