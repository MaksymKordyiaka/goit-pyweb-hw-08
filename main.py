import json
import certifi
from pymongo.mongo_client import MongoClient

client = MongoClient(
    "mongodb+srv://test_db:test@cluster0.1nimxos.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    tlsCAFile=certifi.where()
)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.quotes

if db.authors.count_documents({}) == 0:
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        db.authors.insert_many(authors_data)

if db.quotes.count_documents({}) == 0:
    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = db.authors.find_one({"fullname": quote_data["author"]})
            if author:
                quote_data["author"] = author["_id"]
                db.quotes.insert_one(quote_data)
            else:
                print(f"Author '{quote_data['author']}' not found.")


def find_quotes_by_author(author_name):
    author = db.authors.find_one({"fullname": author_name})
    if author:
        quotes = db.quotes.find({"author": author["_id"]})
        return list(quotes)
    return []


# Функція для пошуку цитат за тегом
def find_quotes_by_tag(tag):
    quotes = db.quotes.find({"tags": tag})
    return list(quotes)


# Функція для пошуку цитат за набором тегів
def find_quotes_by_tags(tags):
    tags_list = tags.split(',')
    quotes = db.quotes.find({"tags": {"$in": tags_list}})
    return list(quotes)


def main():
    while True:
        print('\nExample input:\n'
              '"name: Albert Einstein"\n'
              '"tag: thinking"\n'
              '"tags: miracles,thinking,..."')
        command = input("\nEnter command: ").strip()
        if command.startswith("name:"):
            author_name = command[len("name:"):].strip()
            quotes = find_quotes_by_author(author_name)
            if quotes:
                for quote in quotes:
                    author = db.authors.find_one({"_id": quote["author"]})
                    print(f"{author['fullname']}: {quote['quote']}")
            else:
                print(f"No quotes found for author '{author_name}'.")

        elif command.startswith("tag:"):
            tag = command[len("tag:"):].strip()
            quotes = find_quotes_by_tag(tag)
            if quotes:
                for quote in quotes:
                    author = db.authors.find_one({"_id": quote["author"]})
                    print(f"{author['fullname']}: {quote['quote']}")
            else:
                print(f"No quotes found for tag '{tag}'.")

        elif command.startswith("tags:"):
            tags = command[len("tags:"):].strip()
            quotes = find_quotes_by_tags(tags)
            if quotes:
                for quote in quotes:
                    author = db.authors.find_one({"_id": quote["author"]})
                    print(f"{author['fullname']}: {quote['quote']}")
            else:
                print(f"No quotes found for tags '{tags}'.")

        elif command.startswith('exit'):
            break

if __name__ == '__main__':
    main()
    client.close()
