<!DOCTYPE html>
<html>
  <head>
    <title>Draw Features</title>
    <link rel="stylesheet" href="http://openlayers.org/en/v3.15.1/css/ol.css" type="text/css">
    <script src="http://openlayers.org/en/v3.15.1/build/ol.js"></script>
  </head>
  <body>
    <div id="map" class="map"></div>
    <form class="form-inline">
      <label>Geometry type &nbsp;</label>
      <select id="type">
        <option value="Point">Point</option>
        <option value="LineString">LineString</option>
        <option value="Polygon">Polygon</option>
        <option value="Circle">Circle</option>
        <option value="Square">Square</option>
        <option value="Box">Box</option>
        <option value="None">None</option>
      </select>
    </form>
    <script>
      var raster = new ol.layer.Tile({
        source: new ol.source.MapQuest({layer: 'sat'})
      });

      var source = new ol.source.Vector({wrapX: false});

      var vector = new ol.layer.Vector({
        source: source,
        style: new ol.style.Style({
          fill: new ol.style.Fill({
            color: 'rgba(255, 255, 255, 0.2)'
          }),
          stroke: new ol.style.Stroke({
            color: '#ffcc33',
            width: 2
          }),
          image: new ol.style.Circle({
            radius: 7,
            fill: new ol.style.Fill({
              color: '#ffcc33'
            })
          })
        })
      });

      var map = new ol.Map({
        layers: [raster, vector],
        target: 'map',
        view: new ol.View({
          center: [-11000000, 4600000],
          zoom: 4
        })
      });

      var typeSelect = document.getElementById('type');

      var draw; // global so we can remove it later
      function addInteraction() {
        var value = typeSelect.value;
        if (value !== 'None') {
          var geometryFunction, maxPoints;
          if (value === 'Square') {
            value = 'Circle';
            geometryFunction = ol.interaction.Draw.createRegularPolygon(4);
          } else if (value === 'Box') {
            value = 'LineString';
            maxPoints = 2;
            geometryFunction = function(coordinates, geometry) {
              if (!geometry) {
                geometry = new ol.geom.Polygon(null);
              }
              var start = coordinates[0];
              var end = coordinates[1];
              geometry.setCoordinates([
                [start, [start[0], end[1]], end, [end[0], start[1]], start]
              ]);
              return geometry;
            };
          }
          draw = new ol.interaction.Draw({
            source: source,
            type: /** @type {ol.geom.GeometryType} */ (value),
            geometryFunction: geometryFunction,
            maxPoints: maxPoints
          });
          map.addInteraction(draw);
        }
      }


      /**
       * Handle change event.
       */
      typeSelect.onchange = function() {
        map.removeInteraction(draw);
        addInteraction();
      };

      addInteraction();
    </script>
  </body>
</html>

db.runCommand( {
	geoNear: "Pub3",
	near: {type: "Point", coordinates: [25.5,60.9]},
	spherical: true,
	minDistance: 0,
	maxDistance: 10000
})

db.Pub3.aggregate( [{
	$geoNear: {
	near: {type: "Point", coordinates: [25.5,60.9]},
	distanceField: "dist.calculated",
	minDistance: 0,
	maxDistance: 1000,
	spherical: true
	}
}])
db.Pub3.find({geo:{$near:{$geometry: {type:"Point", coordinates:[24.81, 60.22]},$minDistance: 1000, $maxDistance: 5000}}})
db.Pub3.find({"geo.coordinates": {$exists: true},geo:{$near:{$geometry: {type:"Point", coordinates:[24.81, 60.22]},$minDistance: 1000}}},{"geo.coordinates":1, _id:0}).limit(0)
