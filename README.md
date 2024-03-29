# strawberry-cursor-pagination

# About
Use this project as a base for implementing a Strawberry GraphQL server with pagination. 

This is a small demo python project containing:
- A tiny in-memory mock DB with sample entries and pagination support (limit+cursor)
- An implementation of a Strawberry GraphQL server with pagination for this mock DB

Read [this post](https://medium.com/@keren.duchan/set-up-a-strawberry-graphql-server-with-pagination-python-711c2f4652b2) on Medium for a detailed tutorial about this code.

Refer to the Strawberry Pagination documentation [here](https://strawberry.rocks/docs/guides/pagination#pagination).

# Quickstart

## Install
```
python -m venv virtualenv
source virtualenv/bin/activate
pip install 'strawberry-graphql[debug-server]'
```

## Run the Strawberry GraphQL server
```
strawberry server schema
```
You will get the following message:
```
Running strawberry on http://0.0.0.0:8000/graphql 🍓
```

## Query the server
Go to [http://0.0.0.0:8000/graphql](http://0.0.0.0:8000/graphql) to open **GraphiQL**,
and run the following query to get the first two books:

```
{
  books(first: 2, after: null) {
    pageInfo {
      hasPreviousPage
      hasNextPage
      startCursor
      endCursor
    }
    edges {
      node {
        id
        title
      }
      cursor
    }
  }	
}
```
The result should look like this: 
```
{
  "data": {
    "books": {
      "pageInfo": {
        "hasPreviousPage": false,
        "hasNextPage": true,
        "startCursor": "VGl0bGUgMQ==",
        "endCursor": "VGl0bGUgMg=="
      },
      "edges": [
        {
          "node": {
            "id": "1",
            "title": "Title 1"
          },
          "cursor": "VGl0bGUgMQ=="
        },
        {
          "node": {
            "id": "2",
            "title": "Title 2"
          },
          "cursor": "VGl0bGUgMg=="
        }
      ]
    }
  }
}
```
Note that `hasPreviousPage` is `false`, to indicate that this is the first page.

Get the next two books by running the same query, after changing `after` to be the 
value of `endCursor` received in the result (`"VGl0bGUgMg=="`).

Repeat until `hasNextPage` is `false`.
