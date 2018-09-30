const deckgl = new deck.DeckGL({
  mapboxApiAccessToken: '',
  mapStyle: 'https://free.tilehosting.com/styles/darkmatter/style.json?key=U0iNgiZKlYdwvgs9UPm1',
  longitude: -1.4157,
  latitude: 52.2324,
  zoom: 6,
  minZoom: 3,
  maxZoom: 25,
  pitch: 40.5
});
 
let data = null;

const OPTIONS = ['radius', 'coverage', 'upperPercentile'];

const COLOR_RANGE = [
  [1, 152, 189],
  [73, 227, 206],
  [216, 254, 181],
  [254, 237, 177],
  [254, 173, 84],
  [209, 55, 78]
];

const LIGHT_SETTINGS = {
  lightsPosition: [-0.144528, 49.739968, 8000, -3.807751, 54.104682, 8000],
  ambientRatio: 0.4,
  diffuseRatio: 0.6,
  specularRatio: 0.2,
  lightsStrength: [0.8, 0.0, 0.8, 0.0],
  numberOfLights: 2
};

OPTIONS.forEach(key => {
  document.getElementById(key).oninput = renderLayer;
});

function renderModal(object) {
  console.log(object);
}

function renderLayer () {
  const options = {};
  OPTIONS.forEach(key => {
    const value = document.getElementById(key).value;
    document.getElementById(key + '-value').innerHTML = value;
    options[key] = value;
  });

  const hexagonLayer = new deck.HexagonLayer({
    id: 'heatmap',
    colorRange: COLOR_RANGE,
    data,
    elevationRange: [0, 1000],
    elevationScale: 250,
    pickable: true,
    extruded: true,
    getPosition: d => d,
    lightSettings: LIGHT_SETTINGS,
    opacity: 1,
    onClick: (object => renderModal(object)),
    ...options
  });

  deckgl.setProps({
    layers: [hexagonLayer]
  });
}

d3.csv('https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv',
    (error, response) => {
  data = response.map(d => [Number(d.lng), Number(d.lat)]);
  renderLayer();
});

$(document).ready(function() {
    function toggleSidebar() {
        $(".button").toggleClass("active");
        $("main").toggleClass("move-to-left");
        $(".sidebar-item").toggleClass("active");
        if ($(".button").hasClass("active")) {
            $(".sidebar").css('z-index', 3);
        }
        else
            $(".sidebar").css('z-index', 0);
    }

    $(".button").on("click tap", function () {
        toggleSidebar();
    });

    $(document).keyup(function (e) {
        if (e.keyCode === 27) {
            toggleSidebar();
        }
    });
});