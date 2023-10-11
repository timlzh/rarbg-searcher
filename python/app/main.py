from flask import Flask, render_template, request
import pymongo

client = pymongo.MongoClient("mongodb://db:27017/")
db = client["rarbg"]
col = db["rarbg"]

app = Flask(__name__)


def prettify_size(size):
    if size is None:
        return "Unknown"
    elif size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{round(size / 1024, 2)} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{round(size / 1024 / 1024, 2)} MB"
    else:
        return f"{round(size / 1024 / 1024 / 1024, 2)} GB"

def _search(query, category, skip=0, limit=50):
    categories = ["all", "movies", "tv", "games",
                  "software", "ebooks", "xxx", "music"]
    if category not in categories:
        category = "all"

    if category == "all":
        results = col.find({"$text": {"$search": query}}, {"score": {"$meta": "textScore"}, "title": 1,
                                                           "size": 1, "cat": 1, "hash": 1, "_id": 0}).sort([("score", {"$meta": "textScore"})]).limit(limit).skip(skip)
    else:
        results = col.find({"$text": {"$search": query}, "cat": category}, {"score": {"$meta": "textScore"},
                           "title": 1, "size": 1, "cat": 1, "hash": 1, "_id": 0}).sort([("score", {"$meta": "textScore"})]).limit(limit).skip(skip)

    total_count = results.count()
    results = list(results)
    for result in results:
        result['size'] = prettify_size(result['size'])
        result['hash'] = to_magnet(result['hash'])

    return results, total_count

def to_magnet(hash):
    return f"magnet:?xt=urn:btih:{hash}"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search():
    limit = 20
    query = request.form['query']
    category = request.form['category']
    page = request.form['page']
    page = 1 if page == "" else int(page)

    results, total_count = _search(query, category, skip=(page - 1) * limit, limit=limit)
    max_page = total_count // limit + 1
    return render_template('index.html', results=results, query=query, category=category, page=page, max_page=max_page)

@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/download', methods=['POST'])
def download():
    hashes = request.form.getlist('hashes')
    downloader = request.form['downloader']
    return render_template('download.html', hashes=hashes, downloader=downloader)
    

if __name__ == '__main__':
    print("Checking for title index...")
    print(col.index_information())
    if "title_text" not in col.index_information():
        print("Creating title index...")
        col.create_index([("title", pymongo.TEXT)], name="title_text")
        print("Index created!")

    app.run(host='0.0.0.0', port=5000)
