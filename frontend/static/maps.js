let mymap;

function initMap(x, y, divId) {
    mymap = L.map(divId).setView([x, y], 13);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoibWFjaWVrMSIsImEiOiJja2poYm8zbGk0eG02MnpsZzVsOHF4YWliIn0.T3ME0f2YUNbKvXYRHRrgog'
    }).addTo(mymap);
}


function addMarker(x, y, text, icon) {
    let url, size;

    if (icon === 'alt') {
        url = 'https://cdn2.iconfinder.com/data/icons/bitsies/128/Location-64.png';
        size = [48, 48]
    } else {
        url = 'https://cdn4.iconfinder.com/data/icons/evil-icons-user-interface/64/location-64.png';
        size = [64, 64]
    }

    L.marker([x, y], {icon: L.icon({
        iconUrl: url,
        iconSize: size,
    }), title: text})
        .bindPopup(text)
        .openPopup()
        .addTo(mymap);
}
