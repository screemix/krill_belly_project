from pymongo import MongoClient
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords")
mystem = Mystem()
russian_stopwords = stopwords.words("russian")

def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]

    text = " ".join(tokens)

    return text

client = MongoClient('mongodb+srv://user:user@cluster0-ybcmn.mongodb.net/test?retryWrites=true&w=majority')
cursor = client["bookshop"]["books"].aggregate(
    [
        {
            "$project": {
                "_id": 0,
                "book_id": "$_id",
                "description": "$description"

            }
        },
        {
            "$sort": {
                "book_id": 1,
            }
        }
    ]
)

books_descript = list(cursor)
client.close()

for item in books_descript:
    item['description'] = preprocess_text(item['description'])

books_descript = pd.DataFrame.from_dict(books_descript)

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0)
tfidf_matrix = tf.fit_transform(books_descript['description'])

cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
results = {}
for idx, row in books_descript.iterrows():
   similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
   similar_items = [(cosine_similarities[idx][i], books_descript['book_id'][i]) for i in similar_indices]
   results[row['book_id']] = similar_items[1:]

def item(id):
  return books_descript.loc[books_descript['book_id'] == id]['description'].tolist()[0].split(' - ')[0] # Just reads the results out of the dictionary.def recommend(item_id, num):

def recommend(item_id, num):
    print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")
    print("-------")
    recs = results[item_id][:num]
    for rec in recs:
        print("Recommended: " + item(rec[1]) + " (score:" +      str(rec[0]) + ")")

recommend(item_id=11, num=5)