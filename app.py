from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    articles = []
    error = None

    if request.method == 'POST':
        url = request.form.get('url')

        if not url:
            error = "Please enter a URL"
        else:
            feed = feedparser.parse(url)

            if feed.bozo:
                error = "Invalid RSS feed URL!"
            else:
                for entry in feed.entries[:5]:
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'summary': entry.get('summary', '')
                    })

    return render_template('index.html', articles=articles, error=error)

if __name__ == "__main__":
    app.run(debug=True)