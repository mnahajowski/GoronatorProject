let routeSegments = []
let correlatedSegments = []
let selectedSegment = null
let maxId = 0

function hideCorrelatedModal() {
    document.getElementById("addSegmentModal").style.display = "none"
}

function showCorrelatedModal() {
    document.getElementById("addSegmentModal").style.display = "block"


    if (routeSegments.length > 0) {
        let lastPointId;

        if (routeSegments[routeSegments.length - 1].direction)
            lastPointId = routeSegments[routeSegments.length - 1].point_2
        else
            lastPointId = routeSegments[routeSegments.length - 1].point_1

        if (typeof lastPointId === "object")
            lastPointId = lastPointId.id

        fetch("http://localhost:5001/correlated/" + lastPointId)
            .then(res => res.json())
            .then(data => {
                correlatedSegments = data.segments
                addCorrelatedSegments(data)
            })
    } else
        fetch("http://localhost:5001/segments")
            .then(res => res.json())
            .then(data => {
                correlatedSegments = data.segments
                addCorrelatedSegments(data)
            })

    initSecondaryMap("secondaryMap")
}


function onCorrelatedClick(name, point_1, point_2) {
    let segments = document.getElementsByClassName("correlledSegments");
    for (let segment of segments) {
        if (segment.text === name) {
            segment.style.backgroundColor = "#44AAEE";
            selectedSegment = correlatedSegments[parseInt(segment.getAttribute('data-segment-index'))];
        } else
            segment.style.backgroundColor = "white";
    }

    removeNewMarkers()

    fetch(`http://localhost:5001/point/${point_1},${point_2}`)
            .then(res => res.json())
            .then(points => {
                for (let point of points.points)
                    if (markersOld.findIndex(m => m[2] === point.name) === -1)
                        addMarker(point['x'], point['y'], point['name'], 'red', true)
            })
}

function updateRouteInfo() {
    let routeInfo = document.getElementById('route-info')

    let points = 0, distance = 0, up = 0, down = 0

    for (let segment of routeSegments) {
        if (segment.direction) {
            points += segment.score;
            up += segment.height_diff_up;
            down += segment.height_diff_down;
        } else {
            points += segment.score_reverse;
            up += segment.height_diff_down;
            down += segment.height_diff_up;
        }
        distance += segment.distance;
    }

    routeInfo.textContent = `${points} PKT GOT | ${distance}m <-> | ${up}m ^ | ${down}m v`
}

function reverseName(segment) {
    let split = segment.name.split(' - ');
    segment.name = split[1] + ' - ' + split[0];
}

function addSegment(segment) {
    segment.index = maxId++;

    if (routeSegments.length === 0) {
        if (segment.direction === undefined)
            segment.direction = true

        routeSegments.push(segment)
    } else {
        let last = routeSegments[routeSegments.length - 1]

        if (segment.direction === undefined)
            if (last.direction)
                segment.direction = segment.point_1 === last.point_2;
            else
                segment.direction = segment.point_1 === last.point_1;

        if (!segment.direction)
            reverseName(segment);

        routeSegments.push(segment)
    }
}

function onNewSegmentChoice() {
    addSegment(selectedSegment)

    updateRouteInfo()
    addSegmentsToList()

    fetch(`http://localhost:5001/point/${selectedSegment.point_1},${selectedSegment.point_2}`)
        .then(res => res.json())
        .then(points => {
            for (let point of points.points)
                if (markersOld.findIndex(m => m[2] === point.name) === -1)
                    addMarker(point['x'], point['y'], point['name'], 'blue')
        })

    hideCorrelatedModal()
}

function reverseSegment(index) {
    let segmentIndex = routeSegments.findIndex(s => s.index === index);
    routeSegments = routeSegments.slice(0, segmentIndex + 1).reverse()

    for (let i = 0; i < routeSegments.length; i++) {
        routeSegments[i].direction = !routeSegments[i].direction;
        reverseName(routeSegments[i]);
    }

    updateRouteInfo()
    addSegmentsToList()

    if (secondaryMap === undefined)
        initSecondaryMap('secondaryMap')

    removeOldMarkers()
    removeNewMarkers()

    for (let segment of routeSegments) {
        fetch(`http://localhost:5001/point/${segment.point_1},${segment.point_2}`)
            .then(res => res.json())
            .then(points => {
                for (let point of points.points)
                    addMarker(point['x'], point['y'], point['name'], 'blue')
        })
    }
}

function addSegmentsToList() {
    let segmentList = document.getElementById("route-segments");
    let segmentInfoList = document.getElementById("segment-info-list");

    segmentList.innerHTML = ""
    segmentInfoList.innerHTML = ""

    for (let segment of routeSegments) {
        let newSegment = document.createElement("a");
        newSegment.className = "list-group-item list-group-item-action"
        newSegment.textContent = segment.name
        segmentList.appendChild(newSegment);

        let newElement = document.createElement("li");
        let content = `<img class="arrowImg" src="/static/images/arrow.svg" onclick="reverseSegment(${segment.index})">\n`;

        if (segment.direction)
            content += `<p>${segment.score} pkt GOT | ${segment.distance}m <-> | ${segment.height_diff_up}m ^ | ${segment.height_diff_down}m v</p>`;
        else
            content += `<p>${segment.score_reverse} pkt GOT | ${segment.distance}m <-> | ${segment.height_diff_down}m ^ | ${segment.height_diff_up}m v</p>`;

        newElement.innerHTML = content;
        segmentInfoList.appendChild(newElement);
    }

    let template = document.createElement('template');
    template.innerHTML = '<a id=\"plus-button-holder\" class=\"list-group-item list-group-item-action\" onclick=\"showCorrelatedModal()\">\n' +
    '    <img class=\"plusButton\" src=\"/static/images/plus-solid-black.svg\">\n</a>';
    segmentList.appendChild(template.content.firstChild)
}


function addCorrelatedSegments(segments) {
    segments = segments.segments
    let correlatedList = document.getElementById("correlated-list");
    correlatedList.innerHTML = ""

    let i = 0
    for (let segment of segments) {
        let template = document.createElement('template');
        template.innerHTML = `<a class="list-group-item list-group-item-action correlledSegments" data-segment-index="${i}"
                               onclick="onCorrelatedClick('${segment.name}', ${segment.point_1}, ${segment.point_2})">${segment.name}</a>`
        correlatedList.appendChild(template.content.firstChild)

        i++;
    }
}

function getRouteData() {
    let route = {};

    route.name = document.getElementById('route-name').value;
    route.segments = [];
    route.tourist_id = 1;  // get tourist id
    route.score = 0;

    for (segment of routeSegments) {
        let newSegment = {};
        newSegment.segment_id = segment.id;
        newSegment.direction = segment.direction;
        newSegment.score = segment.direction ? segment.score : segment.score_reverse;

        route.segments.push(newSegment);

        route.score += newSegment.score;
    }
    return route;
}

function saveRoute() {
    let route = getRouteData();

    const url = "http://localhost:5001/new_route";
    const payload = {
        headers: {
            "content-type": "application/json; charset=UTF-8",
        },
        mode: 'no-cors',
        body: JSON.stringify(route),
        method: "POST"
    };

    function redirect() {
        window.location.href = "/routes/1"
    }

    fetch(url, payload)
        .then(res => {
            redirect()
            let icon = document.getElementById('save-icon')
            icon.setAttribute("src", "/static/images/saved-icon.svg")
            icon.onclick = () => 0
            icon.style.cursor = 'default'
        })
}
