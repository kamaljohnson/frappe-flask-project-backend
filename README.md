# API Documentation

# Books

## Get all books

### Request

`GET` request to `/books/all`

### Response

```json
{
  "books": [
      {
        "id": 1,
        "name": "But first support.",
        "description": "Son win return six know teach sometimes political house simple laugh you interview.",
        "author": "Elijah Thomas PhD",
        "img_src": "https://picsum.photos/id/0/200/300",
        "base_fees": 10,
        "popularity": 350,
        "stock": 5
      },
      {
          "id": 2,
          "name": "After heart leave both.",
          "description": "Black protect worker do TV point meeting beautiful half suddenly.",
          "author": "Natasha Brown",
          "img_src": "https://book_cover.jpg",
          "base_fees": 20,
          "popularity": 480,
          "stock": 10
        }
    ]        
}
```

## Get book by ID

### Request

`GET` request to `/books/<books_id>`

### Response

```json
{
  "book": {
    "id": 1,
    "name": "But first support.",
    "description": "Son win return six know teach sometimes political house simple laugh you interview.",
    "author": "Elijah Thomas PhD",
    "img_src": "https://picsum.photos/id/0/200/300",
    "base_fees": 10,
    "popularity": 350,
    "stock": 5
  }   
}
```

## Get popular books

### Request

`GET` request to `/books/popular`

### Response

```json
{
  "popular_books": [
      {
          "id": 2,
          "name": "After heart leave both.",
          "description": "Black protect worker do TV point meeting beautiful half suddenly.",
          "author": "Natasha Brown",
          "img_src": "https://book_cover.jpg",
          "base_fees": 20,
          "popularity": 480,
          "stock": 10
      },
      {
        "id": 1,
        "name": "But first support.",
        "description": "Son win return six know teach sometimes political house simple laugh you interview.",
        "author": "Elijah Thomas PhD",
        "img_src": "https://picsum.photos/id/0/200/300",
        "base_fees": 10,
        "popularity": 350,
        "stock": 5
      }
    ]        
}
```
## Get all issued books
### Request

`GET` request to `/books/issued/all`

### Response

```json
{
  "issued_books": [
      {
        "id": 1,
        "books_detail_id": 20,
        "is_available": false,
        "transactions": [
          {
            "book_instance_id": 1,
            "due_date": "Thu, 03 Jun 2021 00:00:00 GMT",
            "fees": 16,
            "id": 7,
            "issue_date": "Mon, 12 Apr 2021 00:00:00 GMT",
            "member_id": 2,
            "return_date": null,
            "returned": false
          }
        ]
      }
    ]
}
```
## get books issued to member ID

### Request

`GET` request to `/books/issued/<member_id>`

### Response

```json
{
  "issued_books": [
      {
        "id": 1,
        "books_detail_id": 20,
        "is_available": false,
        "transactions": [
          {
            "book_instance_id": 1,
            "due_date": "Thu, 03 Jun 2021 00:00:00 GMT",
            "fees": 16,
            "id": 7,
            "issue_date": "Mon, 12 Apr 2021 00:00:00 GMT",
            "member_id": 2,
            "return_date": null,
            "returned": false
          }
        ]
      }
    ]
}
```

# Members

## Get all members

### Request

`GET` request to `/members/all`

### Response

```json
{
  "members": [
    {
      "books_taken": 7,
      "email": "ritaking@vasquez.net",
      "id": 1,
      "total_paid": 196,
      "transactions": [
        {
          "book_instance_id": 36,
          "due_date": "Tue, 11 May 2021 00:00:00 GMT",
          "fees": 16,
          "id": 10,
          "issue_date": "Mon, 12 Apr 2021 00:00:00 GMT",
          "member_id": 1,
          "return_date": null,
          "returned": false
        }
      ]
    }
  ]
}
    
```

## Get member by ID

### Request

`GET` request to `/members/<member_id>`

### Response

```json
{
  "member": {
    "books_taken": 7,
    "email": "ritaking@vasquez.net",
    "id": 1,
    "total_paid": 196,
    "transactions": [
      {
        "book_instance_id": 36,
        "due_date": "Tue, 11 May 2021 00:00:00 GMT",
        "fees": 16,
        "id": 10,
        "issue_date": "Mon, 12 Apr 2021 00:00:00 GMT",
        "member_id": 1,
        "return_date": null,
        "returned": false
      }
    ],
    "unbilled": 0,
    "username": "davis"
  }
}
    
```

## Create new member

### Request

`POST` request to `/members/create`

```json
{
  "username": "davis",
  "email": "ritaking@vasquez.net"
}
```

### Response

```json
{
  "member": {
    "books_taken": 7,
    "email": "ritaking@vasquez.net",
    "id": 1,
    "total_paid": 196,
    "transactions": [
      {
        "book_instance_id": 36,
        "due_date": "Tue, 11 May 2021 00:00:00 GMT",
        "fees": 16,
        "id": 10,
        "issue_date": "Mon, 12 Apr 2021 00:00:00 GMT",
        "member_id": 1,
        "return_date": null,
        "returned": false
      }
    ],
    "unbilled": 0,
    "username": "davis"
  }
}
    
```

## Delete member

### Request

`GET` request to `/members/delete/<member_id>`

### Response

```json
{
    "msg": "deleted member successfully"
}
```

## Edit member

### Request

`POST` request to `/members/edit/<member_id>`

```json
{
  "username": "davis",
  "email": "ritaking@vasquez.net"
}
```

### Response

```json
{
  "member": {
    "books_taken": 7,
    "email": "ritaking@vasquez.net",
    "id": 1,
    "total_paid": 196,
    "transactions": [
      {
        "book_instance_id": 36,
        "due_date": "Tue, 11 May 2021 00:00:00 GMT",
        "fees": 16,
        "id": 10,
        "issue_date": "Mon, 12 Apr 2021 00:00:00 GMT",
        "member_id": 1,
        "return_date": null,
        "returned": false
      }
    ],
    "unbilled": 0,
    "username": "davis"
  }
}
    
```

# Transactions

## Get all transactions

### Request

`GET` request to `/transactions/all`

### Response

```json
{
  "transactions": [
    {
      "book_instance_id": 14,
      "due_date": "Fri, 27 Nov 2020 00:00:00 GMT",
      "fees": 16,
      "id": 1,
      "issue_date": "Fri, 16 Oct 2020 00:00:00 GMT",
      "member_id": 4,
      "return_date": "Tue, 27 Oct 2020 00:00:00 GMT",
      "returned": true
    },
    {
      "book_instance_id": 17,
      "due_date": "Sun, 10 Jan 2021 00:00:00 GMT",
      "fees": 32,
      "id": 2,
      "issue_date": "Fri, 04 Dec 2020 00:00:00 GMT",
      "member_id": 4,
      "return_date": "Tue, 22 Dec 2020 00:00:00 GMT",
      "returned": true
    },
    {
      "book_instance_id": 12,
      "due_date": "Sun, 08 Nov 2020 00:00:00 GMT",
      "fees": 298,
      "id": 3,
      "issue_date": "Sun, 20 Sep 2020 00:00:00 GMT",
      "member_id": 10,
      "return_date": "Sun, 13 Dec 2020 00:00:00 GMT",
      "returned": true
    },
    {
      "book_instance_id": 26,
      "due_date": "Wed, 09 Dec 2020 00:00:00 GMT",
      "fees": 250,
      "id": 4,
      "issue_date": "Sat, 24 Oct 2020 00:00:00 GMT",
      "member_id": 2,
      "return_date": "Sat, 26 Dec 2020 00:00:00 GMT",
      "returned": true
    }
  ]
}
```

## Issue book

`POST` request to `/transactions/issue_book`

```json
{
  "book_instance_id": 1,
  "member_id": 1,
  "issue_period": 60
}
```

### Response

```json
{
  "transaction": {
     "book_instance_id": 1,
      "due_date": "Sun, 08 Nov 2020 00:00:00 GMT",
      "fees": 298,
      "id": 3,
      "issue_date": "Sun, 20 Sep 2020 00:00:00 GMT",
      "member_id": 1,
      "return_date": "Sun, 13 Dec 2020 00:00:00 GMT",
      "returned": false
  }
}
```

## Return book

`GET` request to `/transactions/return_book/1`

### Response

```json
{
  "transaction": {
     "book_instance_id": 1,
      "due_date": "Sun, 08 Nov 2020 00:00:00 GMT",
      "fees": 298,
      "id": 3,
      "issue_date": "Sun, 20 Sep 2020 00:00:00 GMT",
      "member_id": 2,
      "return_date": "Sun, 13 Dec 2020 00:00:00 GMT",
      "returned": true
  }
}
```

# Reports

## Get all reports

`GET` request to `/library/reports/all`

### Response

```json
{
  "reports": [
    {
      "books_issued": 1,
      "date": "Sat, 08 Aug 2020 00:00:00 GMT",
      "earnings": 0,
      "id": 1
    },
    {
      "books_issued": 0,
      "date": "Sun, 09 Aug 2020 00:00:00 GMT",
      "earnings": 0,
      "id": 2
    },
    {
      "books_issued": 1,
      "date": "Mon, 10 Aug 2020 00:00:00 GMT",
      "earnings": 0,
      "id": 3
    },
    {
      "books_issued": 0,
      "date": "Tue, 11 Aug 2020 00:00:00 GMT",
      "earnings": 0,
      "id": 4
    },
    {
      "books_issued": 1,
      "date": "Wed, 12 Aug 2020 00:00:00 GMT",
      "earnings": 0,
      "id": 5
    },
    {
      "books_issued": 0,
      "date": "Thu, 13 Aug 2020 00:00:00 GMT",
      "earnings": 0,
      "id": 6
    },
    {
      "books_issued": 0,
      "date": "Fri, 14 Aug 2020 00:00:00 GMT",
      "earnings": 0,
      "id": 7
    }
  ]
}
```

## Get report for period

`POST` request to `/library/reports/all`

```json
{
  "from_date": "2021-5-1",
  "till_date": "2021-6-1"
}

```

### Response

```json
{
  "report": {
    "books_issued": 5,
    "books_returned": 3,
    "earnings": 1260
  }
}
```