import os, sqlite3

from flask import Flask, request, session, g, redirect, \
    url_for, abort, render_template, flash

#### config app ####

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'data.db'),
    DEBUG=True,
    SECRET_KEY='temp key',
    USERNAME='iam',
    PASSWORD='smart'
))


#### model ####

def connect_db():
    rv=sqlite3.connect(app.config['DATABASE'])
    rv.row_factory=sqlite3.Row
    return rv

def get_db():
    '''
    if application context g doesn't have db 
    connected then connect
    '''
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db=connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    '''close db at end of request'''
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    '''create tables'''
    with app.app_context():
        db=get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


#### controller - web ####

@app.route('/')
def web_root():
    '''
    show home page
    to do
    '''
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('web_root'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/tags', methods=['GET', 'POST'])
def web_tags():
    '''
    add new tag if POST
    show tag list and add new tag form
    '''
    db=get_db()
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        db.execute('insert into tags (name) values (?)',
            [request.form['newtagname']])
        db.commit()
        flash('new tag added successfully')
        return redirect(url_for('web_tags'))

    #GET
    cur = db.execute('select id, name from tags order by id')
    taglist=cur.fetchall()
    print taglist

    return render_template('show_tags.html', taglist=taglist)


@app.route('/docs', methods=['GET', 'POST'])
def web_docs():
    '''
    show all docs and add new doc form
    add new doc if POST
    '''
    db=get_db()
    if request.method=='POST':
        if not session.get('logged_in'):
            abort(401)
        print 'check1'
        db.execute('insert into docs (title, content, tag_id, \
            upvote, downvote) values (?, ?, ?, 0, 0)', \
            [request.form['title'], request.form['content'], \
            request.form['tagid']])
        print 'check2'
        db.commit()
        print 'check3'
        flash('new doc added successfully')
        return redirect(url_for('web_docs'))
    #GET
    cur=db.execute('select id, title, content, tag_id, \
        upvote, downvote from docs order by id desc')
    doclist=cur.fetchall()

    cur1 = db.execute('select id, name from tags order by id')
    taglist=cur1.fetchall()

    return render_template('show_docs.html', doclist=doclist, \
        taglist=taglist)


@app.route('/tag/<int:tagid>')
def web_tagid(tagid):
    '''
    list all docs with tag tagid
    '''
    db=get_db()
    cur=db.execute("select id, name from tags where id='" + str(tagid) + "'")
    tagname=cur.fetchone()[1]

    cur=db.execute("select id, title, content, tag_id, upvote, downvote \
        from docs where tag_id='" + str(tagid) + "'")
    doclist=cur.fetchall()

    return render_template('show_tag_docs.html', doclist=doclist, \
        tagname=tagname)


@app.route('/doc/<int:docid>', methods=['GET', 'POST'])
def web_docid(docid):
    '''show doc details'''
    db=get_db()
    cur=db.execute("select id, title, content, tag_id, upvote, downvote \
        from docs where id='" + str(docid) + "'")
    doc=cur.fetchone()

    if request.method=='POST':
        if not session.get('logged_in'):
            abort(401)
        #if is upvote
        #db.execute('insert into docs (title, content, tag_id, \
        #    upvote, downvote) values (?, ?, ?, 0, 0)', \
        #    [request.form['title'], request.form['content'], \
        #    request.form['tagid']])
        #db.commit()
        #flash('upvote successfully')
        #else ...
        return redirect(url_for('web_docid'))

    cur=db.execute("select id, name from tags where id='" + str(doc[3]) + "'")
    tag=cur.fetchone()

    return render_template('show_doc_details.html', doc=doc, \
        tag=tag)


'''

@app.route('/recent')
def api_recent():
    from_index = request.args.get('from', '1')
    to_index = request.args.get('to', '10')
    return 'most recent docs from ' + from_index + ' to ' + to_index

@app.route('/imgs')
def api_imgs():
    return '\n'.join(os.listdir("static/img"))

'''

#### 404 customizatiohn ####

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('404')
    return render_template('404.html'), 404


#### controllers api ####
@app.route('/api/tags')
def api_tags():
    pass


if __name__ == '__main__':
    app.run()