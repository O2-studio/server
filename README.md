server
======

###api

- /tags - list all tags
- /tag/<tagname> - #list# docs with tag tagname
- /tag/<tagname>/recent?count=10 - list 10 recent docs of this tag
- /tag/<tagname>/recent?count=5&full=true - return json of all details of 5 recent docs
- /docs - list all docs
- /docs/<docname> - get details of doc docname
- /docs/recent?count=20
- /docs/recent?count=10&full=true
- /docs/popular?count=8&full=true
- /static/img/<imgname>
- /docs/<docname>/voteup
- /docs/<docname>/votedown
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
