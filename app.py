from flask import Flask, render_template, request, redirect, url_for
from gencode import generate_story
from db import save_story, get_all_stories, collection
from bson import ObjectId
import random
import os

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template("landingpage.html")

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    genre = request.form['genre']
    prompt = request.form['prompt']
    max_length = int(request.form['max_length'])
    num_stories = int(request.form['num_stories'])

    stories = generate_story(genre, prompt, max_length=max_length, num_stories=num_stories)

    container_background_url = f"https://picsum.photos/800/250?random={random.randint(1, 1000)}"
    genre_box_images = {
        'action': 'https://tse1.mm.bing.net/th?id=OIP.3NIF1LqzKKUM2_YlIjYBfQHaEo&pid=Api',
        'adventure': 'https://tse1.mm.bing.net/th?id=OIP.80nmvZfe1N9Bppz8qUWArgHaFj&pid=Api',
        'comedy': 'https://tse1.mm.bing.net/th?id=OIP.vFg8gfUomiQZ0Ln1CuDN7QHaEb&pid=Api',
        'fantasy': 'https://tse1.mm.bing.net/th?id=OIP.cCgAd_iVbw1pK3KqUBMgZgHaF7&pid=Api',
        'horror': 'https://tse1.mm.bing.net/th?id=OIP.cFg-4hUqQXl64NoTLJx3gwHaLH&pid=Api'
    }
    box_image_url = genre_box_images.get(genre, "https://via.placeholder.com/800x250")

    story = stories[0] if stories else prompt  # In case generation fails

    save_story(prompt, genre, story)

    return render_template('generated.html',
                           story=story,
                           genre=genre,
                           container_background_url=container_background_url,
                           box_image_url=box_image_url)

@app.route('/continue_story', methods=['POST'])
def continue_story():
    story = request.form['story']
    genre = request.form['genre']

    continued = generate_story(genre, story, max_length=300, num_stories=1)
    full_story = story + " " + continued[0]

    # Optional: Save continuation as new entry
    save_story(story, genre, full_story)

    container_background_url = f"https://picsum.photos/800/250?random={random.randint(1, 1000)}"
    genre_box_images = {
        'action': 'https://tse1.mm.bing.net/th?id=OIP.3NIF1LqzKKUM2_YlIjYBfQHaEo&pid=Api',
        'adventure': 'https://tse1.mm.bing.net/th?id=OIP.80nmvZfe1N9Bppz8qUWArgHaFj&pid=Api',
        'comedy': 'https://tse1.mm.bing.net/th?id=OIP.vFg8gfUomiQZ0Ln1CuDN7QHaEb&pid=Api',
        'fantasy': 'https://tse1.mm.bing.net/th?id=OIP.cCgAd_iVbw1pK3KqUBMgZgHaF7&pid=Api',
        'horror': 'https://tse1.mm.bing.net/th?id=OIP.cFg-4hUqQXl64NoTLJx3gwHaLH&pid=Api'
    }
    box_image_url = genre_box_images.get(genre, "https://via.placeholder.com/800x250")

    return render_template('generated.html',
                           story=full_story,
                           genre=genre,
                           container_background_url=container_background_url,
                           box_image_url=box_image_url)

@app.route('/history')
def history():
    stories = get_all_stories()
    return render_template('history.html', stories=stories)

@app.route('/delete_story', methods=['POST'])
def delete_story():
    story_id = request.form['story_id']
    collection.delete_one({"_id": ObjectId(story_id)})
    return redirect("/history")

@app.route('/delete/<id>')
def delete_story_by_id(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect("/history")
@app.errorhandler(404)
def not_found_error(e):
    return render_template("error.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("error.html"), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
