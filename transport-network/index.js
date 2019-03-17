'use strict';

var ogma = new Ogma({
  container: 'graph-container',
  options: { backgroundColor: null }
});

// always show labels
ogma.styles.addNodeRule({ text: { minVisibleSize: 0 }});


// Constants
var form                   = document.querySelector('#ui');
var mode                   = 'graph';   // initial mode
var modeTransitionDuration = 500;       // geo-graph transition duration
var outlinesColor          = '#dddddd'; // color of radius outlines
var fontSize               = 12;        // font size for the radius marks
var nameToId               = {};        // map station names to node ids
var shortestPathClass      = 'shortestPath';
var LINE_RE                = /(Line|RER)([\d\w]+)/i; // RegExp to match line numbers
var layoutData             = {
                               centralNode: null,
                               radiusDelta: 200
                             };
// canvas for radius outlines
var canvas                 = document.querySelector('#canvas');
var ctx                    = canvas.getContext('2d');
var tilesUrl               = 'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{retina}.png';



/**
 * Format color for the autocomplete and tooltip
 * @param  {String} color Color
 * @param  {String} name  Line name
 * @return {String}
 */
function formatColor(color, name) {
  var code = name.match(LINE_RE)[2];
  return '<span class="line-color" style="background: ' +
    color + '" title="' + name + '">' + code + '</span>';
}


/**
 * Format line information for the station: multiple lines and colors for them
 * @param  {Array<String>|String} colors
 * @param  {String}        lines
 * @return {String}
 */
function formatColors(colors, lines) {
  var linesArray = lines.split('-');
  return Array.isArray(colors)
    ? colors.map(function(color, i) {
        return formatColor(color, linesArray[i])
      }).join('')
    : formatColor(colors, linesArray[0]);
}


/**
 * Reset from radial layout to initial positions
 */
function resetLayout() {
  ogma.clearSelection();
  layoutData.centralNode = null;

  if (layoutData.nodeIds) {
    ogma.getNodes().setAttributes(layoutData.initialPositions);
  }
  renderLayoutOutlines();
}


/**
 * Toggle geo mode on/off
 * @return {Promise}
 */
function toggleGeoMode() {
  if (mode === 'graph') {
    var url = tilesUrl.replace('{retina}', Ogma.utils.getPixelRatio() > 1 ? '@2x' : '');
    console.log(url);
    return ogma.geo.enable({
      latitudePath:    'latitude',
      longitudePath:   'longitude',
      tileUrlTemplate: url,
      duration:        modeTransitionDuration,
      sizeRatio:       0.1
    });
  } else {
    return ogma.geo.disable({ duration: modeTransitionDuration });
  }
}


/**
 * Renders circles outlining the layout layers (orders of graph-theoretical
 * distance)
 * Debounced for smoother rendering.
 */
var renderLayoutOutlines = Ogma.utils.throttle(function renderLayoutOutlines() {
  var w = canvas.width, h = canvas.height;
  ctx.clearRect(0, 0, w, h); // clear screen

  // draw outlines only in graph mode
  if (layoutData.centralNode && mode !== 'geo') {
    var zoom       = ogma.view.getZoom();
    var center     = ogma.view.graphToScreenCoordinates(layoutData.center);
    var pixelRatio = Ogma.utils.getPixelRatio();
    var i, len, distance, radius;

    ctx.lineWidth    = 1;
    ctx.strokeStyle  = outlinesColor;
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'middle';

    center.x *= pixelRatio;
    center.y *= pixelRatio;

    // concentric circles
    ctx.beginPath();
    for (i = 0, len = layoutData.distances.length; i < len; i++) {
      distance = layoutData.distances[i];
      radius = distance * pixelRatio * zoom;

      ctx.moveTo(center.x + radius, center.y);
      ctx.arc(center.x, center.y, radius, 0, 2 * Math.PI, false);
      ctx.moveTo(center.x + radius, center.y);
    }

    ctx.closePath();
    ctx.stroke();

    // label backgrounds
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    for (i = 0, len = layoutData.distances.length; i < len; i++) {
      distance = layoutData.distances[i];
      radius = distance * pixelRatio * zoom;
      ctx.arc(center.x + radius, center.y, fontSize * pixelRatio, 0, 2 * Math.PI, false);
    }
    ctx.fill();

    // label texts
    ctx.fillStyle = outlinesColor;
    ctx.font = fontSize * pixelRatio + 'px sans-serif';
    for (i = 0, len = layoutData.distances.length; i < len; i++) {
      distance = layoutData.distances[i];
      radius = distance * pixelRatio * zoom;
      ctx.fillText(distance / 200, center.x + radius, center.y);
    }
  }
}, 16);


// Add tooltip when hovering the node
ogma.tools.tooltip.onNodeHover(function (node) {
  var color = formatColors(node.getAttribute('color'), node.getData('lines'));
  return '<div class="arrow"></div>' +
         '<div class="ogma-tooltip-header">' +
           '<span class="title">' +
             node.getData('local_name') +
             '&nbsp;' + color +
            '</span>' +
         '</div>';
}, {
  className: 'ogma-tooltip' // tooltip container class to bind to css
});

// Disable the highlight on hover
ogma.styles.setHoveredNodeAttributes(null);


/**
 * Populates UI elements based on received graph data
 * @param  {Object} graph
 */
function populateUI(graph) {
  window.g = graph;
  var stations = graph.nodes.map(function(node) {
    var name = node.data.local_name;
    return {
      label: '<span>' +
               formatColors(node.attributes.color, node.data.lines) +
               '&nbsp;' + name +
             '</span>',
      lines: node.data.lines,
      color: node.attributes.color,
      value: name
    }
  });
  var maxLength = graph.nodes.length;

  createAutocomplete('#from-node-select',    stations, maxLength, onShortestPath);
  createAutocomplete('#to-node-select',      stations, maxLength, onShortestPath);
  createAutocomplete('#central-node-select', stations, maxLength, runLayout);

  var size = ogma.view.getSize();
  canvas.width = size.width * Ogma.utils.getPixelRatio();
  canvas.height = size.height * Ogma.utils.getPixelRatio();
  canvas.style.width = size.width + 'px';
  canvas.style.height = size.height + 'px';
}


/**
 * Shortest path UI callback
 * @param  {Event} evt
 */
function onShortestPath(evt) {
  var source      = form['from-node-select'].value;
  var destination = form['to-node-select'].value;

  ogma.getNodesByClassName(shortestPathClass).removeClass(shortestPathClass);
  ogma.getEdgesByClassName(shortestPathClass).removeClass(shortestPathClass);
  if (source && destination) showShortestPath(source, destination);
}

// Define the class for shortest path representation
// and the attributes associated to it
ogma.createClass(shortestPathClass, {
  nodeAttributes: {
    outerStroke: {
      color: 'red', width: 5
    }
  },
  edgeAttributes: {
    strokeWidth: 5,
    color: 'red'
  }
});


/**
 * Calculate and render shortest path
 * @param  {String} source
 * @param  {String} destination
 */
function showShortestPath(source, destination) {
  if (source !== destination) {
    // calculate and highlight shortest path
    var sourceNode = ogma.getNode(nameToId[source]);
    var destNode   = ogma.getNode(nameToId[destination]);
    var sp         = ogma.pathfinding.dijkstra(sourceNode, destNode);

    // Highlight all the nodes in the shortest path
    if (sp) {
      sp.addClass(shortestPathClass);

      // Get all the edges that connect the nodes of the shortest
      // path together, and highlight them
      sp.getAdjacentEdges().filter(function(edge) {
        return sp.includes(edge.getSource()) &&
               sp.includes(edge.getTarget());
      }).addClass(shortestPathClass);
    }
  }
}


/**
 * Run graph-theoretical distance-based radial layout
 */
function runLayout() {
  if (mode === 'geo') return;
  var newCenter = form['central-node-select'].value;
  if (newCenter && nameToId[newCenter] &&
      layoutData.centralNode !== nameToId[newCenter]) {
    layoutData.centralNode = nameToId[newCenter];

    console.time('radial stress');
    ogma.layouts.radial({
      centralNode:  layoutData.centralNode,
      radiusDelta:  layoutData.radiusDelta,
      duration:     200
    }).then(function () {
      console.timeEnd('radial stress');
      ogma.view.locateGraph({
        easing: 'linear',
        duration: 200
      });
    });
  } else resetLayout();
}


// Load data and init application
ogma.parse.jsonFromUrl('paris-metro.json').then(function (graph) {
  populateUI(graph);
  graph.nodes.forEach(function(node) {
    nameToId[node.data.local_name] = node.id;
  });
  ogma.setGraph(graph);
  ogma.view.locateGraph();


  // clicking on nodes will run the layout, if possible
  ogma.events.onClick(function (evt) {
    if (evt.target && evt.target.isNode) {
      form['central-node-select'].value = evt.target.getData('local_name');
      runLayout();
    }
  });

  // update layout outlines after it's done
  ogma.events.onLayoutComplete(function (evt) {
    // store initial positions
    if (!layoutData.initialPositions) {
      layoutData.initialPositions = evt.positions.before;
      layoutData.nodeIds = evt.ids;
    }
    collectRadii();
  });

  // Update outlines when scene is updated
  ogma.events.onViewChanged(renderLayoutOutlines);
  ogma.events.onDragProgress(renderLayoutOutlines);
  ogma.events.onMouseWheel(renderLayoutOutlines);
});


// Calculates distances of elements from center and stores them to be rendered
// in `renderLayoutOutlines`
function collectRadii() {
  var nodes     = ogma.getNodes();
  var positions = nodes.getPosition();
  var ids       = nodes.getId();
  var center    = ogma.getNode(layoutData.centralNode).getPosition();
  var layers = {};
  for (var i = 0, len = nodes.size; i < len; i++) {
    var pos  = positions[i];
    var dist = Math.round(Ogma.geometry.distance(center.x, center.y, pos.x, pos.y));
    layers[dist] = layers[dist] || [];
    layers[dist].push(ids[i]);
  }
  layoutData.layers    = layers;
  layoutData.center    = center;
  layoutData.positions = positions;
  layoutData.distances = Object.keys(layers).map(function(key) {
    return parseInt(key);
  });
  renderLayoutOutlines();
}


/**
 * Reads mode toggle status from the form
 */
function updateUI() {
  var select = form['mode-switch'];
  var currentMode = Array.prototype.filter.call(select, function(input) {
    return input.checked;
  })[0].value; // IE inconsistency

  if (currentMode !== mode) {
    if (currentMode === 'geo') resetLayout();
    toggleGeoMode().then(function () {
      //ogma.view.locateGraph({ duration: 200 });
      mode = currentMode;
      var layoutPanel = document.querySelector('.toolbar .layout');

      if (mode === 'geo') layoutPanel.classList.add('disabled');
      else {
        layoutPanel.classList.remove('disabled');
        onShortestPath();
        runLayout();
      }
    });
  }

  // onShortestPath();
  // runLayout();
}


// listen for changes on the form
form.addEventListener('change', updateUI);
// disable mouse wheel scroll propagation from UI to Ogma
form.addEventListener('mousewheel', function (evt) {
  event.stopPropagation();
});


/**
 * Creates autocomplet element with eternal library (awesomplete)
 *
 * @param  {String}   selector   DOM selector for input
 * @param  {Array}    data       Stations data
 * @param  {Number}   maxLength  Max items length in list
 * @param  {Function} onSelect   Select item callback
 */
function createAutocomplete(selector, data, maxLength, onSelect) {
  var input    = document.querySelector(selector);
  var select   = new Awesomplete(input, {
    list:      data,
    minChars:  0,
    sort:      function (a,b){
      if (a.value < b.value) return -1;
      if (a.value > b.value) return 1;
      return 0;
    },
    maxItems:  maxLength,
    autoFirst: true,
    item: function (text, input) { // render item with highlighted text
      var html, highlighted;
      if (input.trim() === '') html = text.label; // no changes
      else { // make sure we only replace in contents, not markup
        highlighted = text.value.replace(
          RegExp(Awesomplete.$.regExpEscape(input.trim()), 'gi'),
          '<mark>$&</mark>'
        );
        html = text.label.replace(text.value, highlighted);
      }
      // create DOM element, see Awesomplete documentation
      return Awesomplete.$.create("li", {
        innerHTML: html,
        "aria-selected": "false"
      });
    }
  });

  input.addEventListener('focus', function() {
    select.evaluate();
    select.open();
  });
  input.addEventListener('awesomplete-selectcomplete', function(evt) {
    this.blur();
    onSelect(evt);
  });
}



// Add clear buttons to the search elements
(function() {
  function toggleClear(input, button) {
    button.classList[input.value ? 'remove' : 'add']('hidden');
  }

  function onInputChange(evt) {
    var button = this.parentNode.querySelector('.clear');
    if (!button) button = createButton(this);
    toggleClear(this, button);
  }

  function createButton(input) {
    var button = document.createElement('span');
    var parentNode = input.parentNode;
    button.classList.add('clear');
    button.innerHTML = '&times;';
    if (input.nextSibling) parentNode.insertBefore(button, input.nextSibling);
    else                   parentNode.appendChild(button);
    button.addEventListener('click', function(e) {
      input.value = '';
      toggleClear(input, this);
      onShortestPath();
      runLayout();
    });
    return  button;
  }

  Array.prototype.forEach.call(
    document.querySelectorAll('.clearable-input'), function(input) {
    input.addEventListener('input', onInputChange);
    input.addEventListener('focus', onInputChange);
    input.addEventListener('blur', onInputChange);
  });
})();
