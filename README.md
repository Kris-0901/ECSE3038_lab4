# IoT Water Tanks

## Summary 

This is a RESTful API that allows each IoT enabled water tank to interface with your server so that the measured values can be represented visually on a web page. It interfaces with a system that monitors the status of a set of electronically measured water tanks. The embedded circuit attached to each water tank will measure the height of the water in the tank and report on the tank's current stored volume as a percentage of its maximum capacity.The server is able to perform actions on a resource such as Create, Read, Update and Delete. The data that the API handles and processes is stored in and pulled from a MongoDB database.

*The server's six HTTP routes are:*

- GET `/profile`
- POST `/profile`

- GET `/tank`
- POST `/tank`
- PATCH `/tank/{id}`
- DELETE `/tank/{id}`

*A Profile entity must consist of the following attributes:*

- id
- last_updated
- username
- color
- role

*A Tank entity must consist of the following attributes:*

- id - to be automatically inserted by the server application
- location - The Tank’s location description
- lat - The latitudinal coordinate of the tank
- long - The Longitudinal coordinate of the tank

## Routes & Expected Bahviour 

### Profile Routes

#### **GET `/profile`**
___

*Expected response. If no profile has been added yet:*

- Status Code: `200 OK`

```json
{}
```

*Expected response. If profile has been added:*

- Status Code: `200 OK`

```json
{
    "_id": "67bbb20b253f0ecdab7c2b76",
    "last_updated": "February 23,2025 06:40 PM EST",
    "username": "kris0901",
    "role": "Engineer",
    "color": "#d88e0e"
}
```

#### **POST `/profile`**
___

*Expected request:*
```json
{
    "username": "kris0901",
    "role": "Engineer",
    "color": "#d88e0e"
}
```

*Expected response:*

- Status Code: `201 OK`

```
{
    "id": "67bbb20b253f0ecdab7c2b76",
    "last_updated": "2/3/2022, 8:48:51 PM",
    "username": "kris0901",
    "role": "Engineer",
    "color": "##d88e0e"
}
```

### Tank Routes

### GET `/tank`
___


*Expected Response. If an object has not been POSTed yet*

- Status Code: `200 OK`

```json
[]
```

*Expected Response.  If an object had been previously POSTed*

- Status Code: `200 OK`

```json

[
    {
	"id": "0cf996c3-d9ca-4c0b-ab01-52b26c9050ec",
    "location": "Engineering department",
    "lat": "18.0051862",
    "long": "-76.7505108",
    },
    .
    .
    .
]

```

### POST `/tank`
___

*Expected Request:*

```json
{
    "location": "Physics department",
    "lat": 18.004741066082236,
    "long": -76.74875280426826
}

```

*Expected Response:*

- Status Code: `201 Created`

```json
{
    "id": "2ecc8f75-7594-4383-ac59-a24aff085cb3"
    "location": "Physics department",
    "lat": "18.004741066082236",
    "long": "-76.74875280426826"
}

```
### PATCH `/tank/{id}`
___

*Expected Request:*

```json
{
    "location": "<new location>", //optional
    "lat": "<new lat>", //optional
    "long": "<new long>", //optional
}

```

*Expected Response:*

- Status Code: `200 OK`

```json
{
    "id": "<id>",
    "location": "<updated location>",
    "lat": "<updated lat>",
    "long": "<updated long>",
}

``` 
*Expected Response if API is unable to locate object:*

- Status Code: `404 Not Found`

```json
{
	"detail":"Tank with id: '2ecc8f75-7594-4383-ac59-a24aff085cb3' not found"
}

```

### DELETE `/tank/{id}`
___

*Expected Response:*

- Status Code: `204 No Content`

*Expected Response if API is unable to locate object:*

- Status Code: `404 Not Found`

```json
{
	"detail":"Tank with id: '2ecc8f75-7594-4383-ac59-a24aff085cb3' not found"
}

```

## Purpose

This code was written to fulfill the course requirements of 'ECSE3038 Engineering Internet of Things Systems' and to
learn the Python programming language and RESTful API server.

## Favourite Low Effort Food

Pork chops and fries. Seems fancy but actaully really simple and tasty. 
