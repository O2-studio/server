server
======

access here [http://fierce-meadow-3934.herokuapp.com/](http://fierce-meadow-3934.herokuapp.com/)

###api

- GET /tags - list all tags
- GET /tag/\<tagname\> - _list_ docs with tag tagname
- GET /tag/\<tagname\>/recent?from=1&to=10
- GET /tag/\<tagname\>/recent?from=5&to=7&full=true
- GET /docs - list all docs
- GET /doc/\<docid\> - get details of doc docid
- GET /doc/recent?from=11&to=20
- GET /doc/recent?from=11&to=20&full=true
- GET /doc/popular?from=11&to=20&full=true
- GET /static/img/\<imgname\>
- POST /doc/\<docid\>/voteup
- POST /doc/\<docid\>/votedown
- POST /submit


###doc

```json
{
  "id": "doc id 1,2,3,...",
  "name": "doc name",
  "ctime": "creation time",
  "tags": [
    "tag1 name",
    "tag2 name"
  ],
  "voteup": 10,
  "votedown": 3,
  "data": "doc content",
  "comments": [
    "comment 1",
    "comment 2"
  ]
}
```
