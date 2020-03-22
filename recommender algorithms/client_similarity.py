from pymongo import MongoClient

def Jaccard_similarity(arr1, arr2):

    # Jaccard similarity coefficient is the number of elements in intersection divided on  the number of elements in union
    # where the sets we make intersection and union on are vectors of films watched by two customers
    inersection = 0
    union = 0

    if sum(arr1) == 0 or sum(arr2) == 0:
        return 0

    for i in range(len(arr1)):
        if arr1[i] == 1 and arr2[i] == 1:
            inersection += 1
        if arr1[i] == 1 or arr2[i] == 1:
            union += 1
    return float(inersection)/(float(union))

client = MongoClient('mongodb+srv://user:user@cluster0-ybcmn.mongodb.net/test?retryWrites=true&w=majority')

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

customer_list = list(cursor)

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

book_list = list(cursor)
client.close()

adjacency_matrix = [[0 for i in range(len(book_list))] for j in range(len(customer_list))]
print(adjacency_matrix)
for c in customer_list:
    for item in c['raiting']:
        if (-1)*(3 - item['grade']) > 0:
            adjacency_matrix[c['id']][item['book_id']] = 1

needed_client_id = 2
recommend_list = []
for item in customer_list:
    if item['id'] != needed_client_id:
        recommend_index = Jaccard_similarity(adjacency_matrix[needed_client_id], adjacency_matrix[item['id']])
        recommend_list.append({"customer_id": item['id'], "recommend_index": recommend_index})

recommend_list = sorted(recommend_list, key = lambda i: i['recommend_index'])
recommend_list.reverse()
print('More similar client to one with id ', needed_client_id, ' is client with id ', recommend_list[0]['customer_id'])
