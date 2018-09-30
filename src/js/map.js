const deckgl = new deck.DeckGL({
  mapboxApiAccessToken: '',
  mapStyle: 'https://free.tilehosting.com/styles/darkmatter/style.json?key=U0iNgiZKlYdwvgs9UPm1',
  longitude: -30.090875,
  latitude: 18.587923,
  zoom: 2,
  minZoom: 2,
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


function toggleSidebar(object) {
  populateArticles(object);
  $(".button").toggleClass("active");
  $("main").toggleClass("move-to-left");
  $(".sidebar-item").toggleClass("active");
  if ($(".button").hasClass("active")) {
      $(".sidebar").css('z-index', 3);
  }
  /*else
      $(".sidebar").css('z-index', 0);*/
}

$(document).ready(function() {
  // $(".button").on("click tap", function () {
  //     toggleSidebar();
  // });


  $(document).keyup(function (e) {
      if (e.keyCode === 27) {
          toggleSidebar();
      }
  });
});

function clickOpenSidebar() {
  toggleSidebar();
}

function renderModal(object) {
  toggleSidebar(object);
}

function populateArticles(object) {
    if(object == null)
        return;
    $("#articles").empty();
    var coords = new Set();
    var unique = new Set();
    for(var e in object.object.points) {
        var obj = {
            url: object.object.points[e][2],
            title: object.object.points[e][3],
            pic: object.object.points[e][4],
            sentiment: object.object.points[e][5]
        };
        if(!unique.has(obj.url)) {
            coords.add(obj);
            unique.add(obj.url);
        }
    }
    coords = Array.from(coords);
    for(var c in coords) {
        if(coords[c].title == null)
            continue;
        $("#articles")
            .append('<li><div id="article_'+c+'" class="sidebar-item"><div>' +
                '<img style="width: 70px; height: 70px; margin-right:10px; border-radius: 10px" src='+coords[c].pic+'></div>' +
                '<div><a target="_blank" href="'+coords[c].url+'" class="sidebar-anchor article_href">'+coords[c].title+'</a></div></div></li>');
        if(coords[c].sentiment < 0) {
            $('#article_'+c).css('background-color', '#aa1414');
        }
    }
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


d3.csv('https://raw.githubusercontent.com/jamesw8/news-map.io/master/src/data/articles.csv?token=ARzl-lkZ2-cLQ55oC9AEWO6vfmTrc46Dks5budGiwA%3D%3D',
    (error, response) => {
  data = response.map(d => [Number(d.lng), Number(d.lat), String(d.url), String(d.title), String(d.pic), Number(d.sentiment)]);
  renderLayer();
});