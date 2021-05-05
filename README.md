# Indoor map with LeafletJS

## Idea and Planning of the project
The main purpose of the project was to develop a web interface to locate the sensors according to their latitude and longitude and display the real time data received from them in a web map. The sensors are situated in a selected room and they send the data via web socket and that data is received on client side with the help of python program. The data sent by the sensors includes the information regarding the height, temperature, geo location, time, and temperature of the room. This project would enable the study of the condition of rooms remotely which can help while reacting in emergency such as fire accidents.  

## Tool and Library used
#### 1. LeafletJs
It is an open source JavaScript library which provides many features need for the developers. More explanations about LeafletJS is included below. 
To explore more visit their official website: [LeafletJS](https://leafletjs.com/)

#### 2. Leaflet-indoor
Leaflet indoor plugin provides basic tools to create indoor map with different floor levels with leaflet. If you want to see this plug-in action visit this link to see the demo
[here](https://www.cbaines.net/projects/osm/leaflet-indoor/examples/)

#### 3. Zeromq
Zeromq is an open source messaging library known for its high performance. It supports all the common messaging patterns (pub/sub, request/reply, client/server and other) over a variety of transports. For this project Pub/Sup sockets was used. PUB/SUB stands for ‘publish’ and ‘subscribe’. In this model a PUB socket pushes the message out and all the associated SUB sockets receive those messages and this communication is one way.
To explore more visit its home page [ZeroMQ](https://zeromq.org/)

## How to use ZeroMQ with Python
Zeromq was used to send and receive the data via pub/sub socket. 
To import zeromq in python just need to add one line of code at the top of file

```python
import zeromq
```

To initialize the transferring of data with zeromq from sender i.e in our case send_data.py file,

```python
ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)
sock.connect("tcp://127.0.0.1:8000")
```

To initialize the transferring data with zeromq in receiver side in our case receiver.py file

```python
context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:8000')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
```

At the receiver side data is received with socket and saved in the file data2.json

```python
data = json.loads(message)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)
        data_file = 'data2.json'
        with open(data_file, 'w+') as f:
            f.write(s)
```

## Leaflet introduction

Leaflet is an open source javaScript library for the interactive map. It provides almost all the necessary mapping features within about 39KB of JS.
To make sure leaflet works, its css file and js file should be added in the head section of your document. 
Leaflet CSS file link: 

```html
 <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
   integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
   crossorigin=""/>
```
Leaflet JS file;

```html
 <!-- Make sure you put this AFTER Leaflet's CSS -->
 <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
   integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
   crossorigin=""></script>
```
Once these files are referenced now create a div where you want to display a map.

```html
<div id="map"></div>
```

To add the marker, create a variable called marker

```html
var marker = L.marker([65.06, 25.46]).addTo(map);
```

The numbers 65.06 and 25.46 are the latitude and longitude value. 
It is also possible to add other things, such as circle and polygon to the map.
For more detail check the link [Leaflet-quick-start-guide](https://leafletjs.com/examples/quick-start/)

## Create the map

For the map features Leaflet is used with openstreetmap which is free to use. Visit its official page to explore it more.[Openstreetmap](https://www.openstreetmap.org)

```html
var osmUrl = '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            osm = new L.TileLayer(osmUrl, {
                maxZoom: 22,
                attribution: "Map data &copy; OpenStreetMap contributors"
            });

        var map = new L.Map('map', {
            layers: [osm],
            center: new L.LatLng(65.061, 25.467),
            zoom: 19
        });
```

For indoor, leaflet indoor plugin was used to develop indoor corridors and rooms.
Leaflet indoor plugin provides tools to create the indoor map with leaflet.
For more detail and use visit the link. 
https://github.com/cbaines/leaflet-indoor

For creating latitude and longitude mapbox.com or geojson.io can be used.
Here is sample data created using geojson.io that represent a straight line.

```html 
{
    "type": "FeatureCollection",
    "features": [
      {
          ........
          ........    
   "geometry": {
          ........
          ........
          "coordinates": [
            [
              25.463910698890686,
              65.05917831233543
            ],
            [
              25.464447140693665,
              65.05917831233543
            ]
          ]
        }
      }
    ]
}
```

## Demo Product

Here is the user-interface of the web map. The markers are the location of the sensors and the popup information is real time information and received from the sensors.
The web user interface was developed using JavaScript. 

![](https://github.com/t6nesu00/indoor-map/blob/main/map-product.jpg)

The information in the popups are added from data2.json file where sensor messages are stored.
```javascript
 $.getJSON("data2.json", function(data) {
             ...............
            // lines of code to create the marker and add information
            // from data2.json file      
            ................
        }); 

```

Below data is the sample data send by the sensors, the data is changed to make it usable for JavaScript and saved in data2.json file.

{'payload': {'temperature': '40.21'}, 'latitude': '65.06069728830542', 'height': '5', 'level': '1', 'longitude': '25.46535061690912', 'deviceID': 'Raspberry project', 'timestamp': '1619812597.9148433'}

By default, leaflet does not allow to display two popups simultaneously. To enable this feature use following lines of code.

```javascript
// displaying multiple popups at same time
            L.Map = L.Map.extend({
            openPopup: function(popup) {
                // this.closePopup(); 
                this._popup = popup;

                return this.addLayer(popup).fire('popupopen', {
                    popup: this._popup
                });
            }
            });
```

## Possibile improvements

The coordinates (Latitude and Longitude) of rooms are generated using http://geojson.io however these are not hundred percent accurate. There is possibility that these values can be tested and altered with small differences to make it accurate. 
The user interface is still not finalized this is just the demo to ensure the working of sensors with real time data. The user interface could be changed to more friendly and stylish view.
The format of json file should match exactly with the data present in data2.json otherwise popups will have error while displaying the data. This arises the complexity in case sensor data format are changed or modified. 




