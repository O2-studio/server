import os, sqlite3

from flask import Flask, request, session, g, redirect, \
    url_for, abort, render_template, flash, jsonify

#### config app ####

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'data.db'),
    #DEBUG=True, #comment out in production
    SECRET_KEY='temp key',#replace in prod
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
    if application context g doesn't have db connected
    then connect
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
    add new tag when POST
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
    if 'json' != request.args.get('format'):
        return render_template('show_tags.html', taglist=taglist)
    else:
        ts=[]
        for i in taglist:
            ts.append({"id":i[0], "name":i[1]})
        return jsonify({'tags':ts})

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
        db.execute('insert into docs (title, content, tag_id, \
            upvote, downvote) values (?, ?, ?, 0, 0)', \
            [request.form['title'], request.form['content'], \
            request.form['tagid']])
        db.commit()
        flash('new doc added successfully')
        return redirect(url_for('web_docs'))
    #GET
    cur=db.execute('select id, title, content, tag_id, \
        upvote, downvote from docs order by id desc')
    doclist=cur.fetchall()
    cur = db.execute('select id, name from tags order by id')
    taglist=cur.fetchall()
    if 'json' != request.args.get('format'):
        return render_template('show_docs.html', doclist=doclist, \
            taglist=taglist)
    else:
        ds=[]
        for i in doclist:
            ds.append({"id":i[0], "title":i[1], "tag_id":i[3], \
                    "upvote":i[4], "downvote":i[5]})
        return jsonify({'docs' : ds})

@app.route('/tag/<int:tagid>')
def web_tagid(tagid):
    '''
    list all docs with tag tagid
    '''
    db=get_db()
    cur=db.execute("select id, name from tags where id=?", \
            [str(tagid)])
    tagname=cur.fetchone()[1]
    cur=db.execute("select * from (select id, title, content, \
        tag_id, upvote, downvote from docs where tag_id=?) \
        order by id desc", [str(tagid)])
    doclist=cur.fetchall()
    if 'json' != request.args.get('format'):
        return render_template('show_tag_docs.html', \
            doclist=doclist, tagname=tagname)
    else:
        ds=[]
        for i in doclist:
            ds.append({"id":i[0], "title":i[1], "tag_id":i[3], \
                    "upvote":i[4], "downvote":i[5]})
        return jsonify({'docs' : ds, 'tagid': tagid, \
            'tagname':tagname})

@app.route('/doc/<int:docid>')
def web_docid(docid):
    '''show doc details'''
    db=get_db()
    cur=db.execute("select id, title, content, tag_id, upvote, \
        downvote from docs where id=?", [str(docid)])
    doc=cur.fetchone()
    cur=db.execute("select id, name from tags where id=?", \
            [str(doc[3])])
    tag=cur.fetchone()
    if 'json' != request.args.get('format'):
        return render_template('show_doc_details.html', doc=doc, \
            tag=tag)
    else:
        return jsonify({'id':doc[0], 'title':doc[1], \
                'content':doc[2], 'tag_id':doc[3], \
                'upvote':doc[4], 'downvote':doc[5], \
                'tagname':tag[1]})

@app.route('/doc/<int:docid>/upvote')
def web_upvote(docid):
    '''upvote++'''
    db=get_db()
    cur=db.execute("select id, upvote from docs where id=?", \
            str(docid))
    uv=cur.fetchone()[1]
    db.execute('update docs set upvote=? where id=?', \
            [str(uv+1), str(docid)])
    db.commit()
    flash('upvote successfully')
    if 'json' != request.args.get('format'):
        return redirect(url_for('web_docid', docid=docid))
    else:
        return jsonify({'newupvote':uv+1})


@app.route('/doc/<int:docid>/downvote')
def web_downvote(docid):
    '''downvote++'''
    db=get_db()
    cur=db.execute("select id, downvote from docs where id=?",\
            str(docid))
    dv=cur.fetchone()[1]
    db.execute('update docs set downvote=? where id=?', \
            [str(dv+1), str(docid)])
    db.commit()
    flash('downvote successfully')
    if 'json' != request.args.get('format'):
        return redirect(url_for('web_docid', docid=docid))
    else:
        return jsonify({'newdownvote':dv+1})

@app.route('/doc/recent')
def web_doc_recent():
    '''
    begin and end are not ids
    they are the index of doc sort by id desc
    from 1 to doc count
    '''
    begin = request.args.get('begin', '1')
    end = request.args.get('end', '10')
    db=get_db()
    cur=db.execute("select id, title, content, tag_id, upvote, \
        downvote from docs order by id desc limit ? offset ?", \
        [str(int(end)-int(begin)+1), str(int(begin)-1)])
    doclist=cur.fetchall()
    if 'json' != request.args.get('format'):
        return render_template("show_recent_docs.html", \
            doclist=doclist, begin=begin, end=end)
    else:
        ds=[]
        for i in doclist:
            ds.append({"id":i[0], "title":i[1], 'content':i[2], \
                    "tag_id":i[3], "upvote":i[4], "downvote":i[5]})
        return jsonify({'docs' : ds})

@app.route('/imgs')
def web_imgs():
    return '\n'.join(os.listdir("static/img"))

#### 404 customizatiohn ####

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('404')
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0')
