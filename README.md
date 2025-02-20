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
- username
- color
- role

*A Tank entity must consist of the following attributes:*

- id - to be automatically inserted by the server application
- location - The Tank’s location description
- lat - The latitudinal coordinate of the tank
- long - The Longitudinal coordinate of the tank