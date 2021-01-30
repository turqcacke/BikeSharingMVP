# BikeSharingMVP
MVP for BikeSharing porject

# STATION
### Available requests: **GET**(with auth)
Statuses:
- 0: Occupied
- 1: Active
- 2: Maintenance
**GET**- if succeed status_code=200 else status_code=4000
Return list of stations.
```
http://dev.polito.uz/api/station/
```
```
GET[with auth]

id: int
status: int
longitude: double
latitude: double
bike_place: StationObject
```

---

# ORDERS
### Available requests: **GET**, **POST**(with auth)
If succeed status_code=200 else status_code=4000
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
GET

id: int
user: str (username)
status: int
start: str
end: int or null
bike: int
```

```
POST[with auth]

status: int
bike: int
```
