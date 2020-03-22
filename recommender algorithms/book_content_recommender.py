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
cursor = client["bookshop"]["book"].aggregate(
    [
        {
            "$project": {
                "_id": 0,
                "book_id": "$_id",
                "title": "$title",
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

books = []
for item in cursor:
    books.append(item)

cursor = client["bookshop"]["customer"].aggregate(
    [
        {
            "$project": {
                "_id": 0,
                "id": "$_id",
                "raiting": "$book_raiting"

            }
        },

    ]
)


customer = []
for item in cursor:
    customer.append(item)
client.close()

for item in books:
    item['description'] = preprocess_text(item['description'])

books_descript = pd.DataFrame.from_dict(books)

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

def recommend_book(item_id, num):
    rec =  results[item_id][:num]
    output = []
    for elem in (rec):
        output.append(elem)
    return output

def recommend_to_client(client_id):
    cust = {}
    for item in customer:
        if item['id'] == client_id:
            cust = item
            break

    best_books = []
    for item in cust['raiting']:
        weigth = (-1)*(3 - item['grade'])
        if weigth > 0:
            rec = recommend_book(item_id=item['book_id'], num=5)
            weigthed_rec = []
            for elem in rec:
                weigthed_rec.append((elem[0] * weigth, elem[1]))
            best_books = best_books + weigthed_rec
    best_books = sorted(best_books, key=lambda tup: tup[0])
    best_books.reverse()
    best_books = best_books[0:3]
    return best_books


a = recommend_to_client(0)

print('Recommended books for clients with this id:')
for item in a:
    for elem in books:
        if elem['book_id'] == item[1]:
            print('id of a book: ', elem ['book_id'], ' title: ',  elem['title'])
