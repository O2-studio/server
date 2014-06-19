server
======

###api

- /tags - list all tags
- /tag/\<tagname\> - #list# docs with tag tagname
- /tag/\<tagname\>/recent?count=10 - list 10 recent docs of this tag
- /tag/\<tagname\>/recent?count=5&full=true - return json of all details of 5 recent docs
- /docs - list all docs
- /doc/\<docname\> - get details of doc docname
- /doc/recent?count=20
- /doc/recent?count=10&full=true
- /doc/popular?count=8&full=true
- /static/img/\<imgname\>
- /doc/\<docname\>/voteup
- /doc/\<docname\>/votedown
- POST /submit


###doc

```json
{
  "name": "doc name",
  "fullname": "doc full name for displaying",
  "ctime": "creation time",
  "tags": [
    "tag1 name",
    "tag2 name"
  ],
  "voteup": 10,
  "votedown": 3,
  "data": "doc content"
}
```
