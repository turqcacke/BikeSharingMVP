# BikeSharingMVP
MVP for BikeSharing project

# BASE INFORMATION
If succeed **status_code=20X** else **status_code=40X**
For auth use base auth header

https://en.wikipedia.org/wiki/Basic_access_authentication

##### Authenticate: Basic {base64 login:password}
base64 - base64 encryption should encrypt string "login:password"

**Example:**
```
Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
```

# ORDER
### Available requests: **GET**
Balance statuses:
- 0: Blocked
- 1: Active

**GET** - return user instance

```
http://dev.polito.uz/api/user/
http://dev.polito.uz/api/{username}/

username - username or card number
```

```
GET PARAMS

id: id
user: string (username)
email: string
```

# STATION
### Available requests: **GET**(with auth)
Statuses:
- 0: Occupied
- 1: Active
- 2: Maintenance

**GET**- return list of stations.
```
http://dev.polito.uz/api/station/
```
```
GET PARAMS[with auth]

id: int
status: int
longitude: double
latitude: double
```

---

# ORDERS
### Available requests: **GET**, **POST**(with auth)
If succeed **status_code=200** else **status_code=400**
Statuses:
- 0: Pending
- 1: Active
- 2: Finished

**GET** - return list of user orders if uthenticated else return full list of orders.

**POST** - create new order if suceed return created object

```
http://dev.polito.uz/api/order/
```
```
GET PARAMS

id: int
user: str (username)
status: int
start: string
end: int or null
bike: int (bike id)
```

```
POST PARAMS[with auth]

status: int
bike: int (bike id)
```

---

# BIKE PLACE
### Available requests: **GET**(with auth)
Statuses:
- 0: Occupied
- 1: Active
- 2: Maintenance

**GET** - return list of bike places
```
http://dev.polito.uz/api/bike_place/
```

```
GET PARAMS

id: int
status: int
station: int (station id)
bike: int (bike id)
```
