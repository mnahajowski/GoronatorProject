let routeSegments = []
let maxId = 0

function hideModal() {
    document.getElementById("addSegmentModal").style.display = "none"
}

function showModal() {
    document.getElementById("addSegmentModal").style.display = "block"

    initSecondaryMap("secondaryMap")
}

function changeBackground(newSegment) {
    let segments = document.getElementsByClassName("correlledSegments");
    for (let segment of segments) {
        if (segment.text === newSegment) {
            segment.style.backgroundColor = "#44AAEE";
        } else {
            segment.style.backgroundColor = "white";
        }
    }
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
        segment.direction = true
        routeSegments.push(segment)
    } else {
        let last = routeSegments[routeSegments.length - 1]
        if (last.direction)
            segment.direction = segment.point_1 === last.point_2;
        else {
            segment.direction = segment.point_1 === last.point_1;
            reverseName(segment);
        }

        routeSegments.push(segment)
    }
}

function reverseSegment(index) {
    let segmentIndex = routeSegments.findIndex(s => s.index === index);
    let segment = routeSegments[segmentIndex];
    segment.direction = !segment.direction;
    reverseName(segment)

    routeSegments = routeSegments.slice(0, segmentIndex + 1)

    updateRouteInfo()
    addSegmentsToList()
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
    template.innerHTML = '<a id=\"plus-button-holder\" class=\"list-group-item list-group-item-action\" onclick=\"showModal()\">\n' +
    '    <img class=\"plusButton\" src=\"/static/images/plus-solid-black.svg\">\n</a>';
    segmentList.appendChild(template.content.firstChild)
}
