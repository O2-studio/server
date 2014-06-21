import os

from flask import Flask, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def api_root():
    return render_template('index.html')

@app.route('/tags')
def api_tags():
	return 'List of tags'

@app.route('/tag/<int:tagid>')
def api_tagid(tagid):
	return 'list of docs with tag' + str(tagid)

@app.route('/docs')
def api_docs():
    return 'List of all ' + url_for('api_docs')

@app.route('/doc/<int:docid>')
def api_docid(docid):
    return 'show doc ' + str(docid)

@app.route('/doc/<int:docid>/upvote', methods=['GET', 'POST'])
def api_upvote(docid):
    if request.method == 'POST':
        return "upvote++ for doc " + str(docid)
    else:
        return 'show upvote of ' + str(docid)

@app.route('/recent')
def api_recent():
    from_index = request.args.get('from', '1')
    to_index = request.args.get('to', '10')
    return 'most recent docs from ' + from_index + ' to ' + to_index

@app.route('/imgs')
def api_imgs():
    return '\n'.join(os.listdir("static/img"))


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('404')
    return render_template('404.html'), 404

if __name__ == '__main__':
    #make sure to comment this out in production!
    app.debug = True
    app.run()