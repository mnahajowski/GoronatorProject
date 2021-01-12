let mainMap;
let secondaryMap;
let markersOld = [];
let markersNew = [];

let oldX, oldY;

function initMap(x, y, divId) {
    oldX = x;
    oldY = y;
    mainMap = L.map(divId).setView([x, y], 13);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoibWFjaWVrMSIsImEiOiJja2poYm8zbGk0eG02MnpsZzVsOHF4YWliIn0.T3ME0f2YUNbKvXYRHRrgog'
    }).addTo(mainMap);
}

function initSecondaryMap(divId) {
    secondaryMap = L.map(divId).setView([oldX, oldY], 13);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoibWFjaWVrMSIsImEiOiJja2poYm8zbGk0eG02MnpsZzVsOHF4YWliIn0.T3ME0f2YUNbKvXYRHRrgog'
    }).addTo(secondaryMap);

    for (let marker of markersOld)
        marker.addTo(secondaryMap)
}


function addMarker(x, y, text, color, toNew) {
    let url;

    if (color === 'green')
        url = '/static/images/marker-green.svg';
    else if (color === 'red')
        url = '/static/images/marker-red.svg';
    else
        url = '/static/images/marker-blue.svg';

    var marker = L.marker([x, y], {icon: L.icon({
        iconUrl: url,
        iconSize: [48, 48],
    }), title: text})
        .bindPopup(text)
        .openPopup();

    if (toNew === true) {
        markersNew.push(marker);
        marker.addTo(secondaryMap);
    } else {
        markersOld.push(marker);
        marker.addTo(mainMap);
    }
}


function removeNewMarkers() {
    for (let marker of markersNew)
        secondaryMap.removeLayer(marker);
}