from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/categories')
def api_categories():
    return 'List of ' + url_for('api_categories')

@app.route('/categories/<categoryid>')
def api_category(categoryid):
    return 'List of articles of category ' + \
            categoryid

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

@app.route('/articles/<articleid>/upvote')
def api_upvote(articleid):
    return str(5 + int(articleid))

if __name__ == '__main__':
    app.run()
