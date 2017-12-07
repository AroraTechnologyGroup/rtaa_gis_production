define([
    "esri/request",
    "esri/toolbars/draw",
    "esri/graphic",
    "esri/symbols/SimpleMarkerSymbol",
    "esri/symbols/SimpleLineSymbol",
    "esri/symbols/SimpleFillSymbol",
    "esri/tasks/query",
    "esri/SpatialReference",
    "esri/geometry/Polygon",
    "esri/dijit/PopupTemplate",
    "esri/layers/FeatureLayer",
    "esri/Color",
    "esri/tasks/FeatureSet",

    "dojo/_base/declare",
    "dojo/_base/array",
    "dojo/_base/lang",

    "dojo/dom-construct",
    "dojo/dom",
    "dojo/on",
    "dojo/json",
    "dojo/topic",
    "dojo/request/xhr",
    "dojo/request/script",
    "dojo/request",
    "dojo/promise/all",
    "dojo/Deferred",
    "dojo/cookie",
    "dojo/parser",
    
    "dijit/registry",
    "dijit/form/Button",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dojo/text!./templates/drawToolbar.html",
    "dojo/NodeList-traverse"
], function (
    esriRequest,
    Draw,
    Graphic,
    SimpleMarkerSymbol,
    SimpleLineSymbol,
    SimpleFillSymbol,
    Query,
    SpatialReference,
    Polygon,
    PopupTemplate,
    FeatureLayer,
    Color,
    FeatureSet,

    declare,
    Array,
    lang,

    domConstruct,
    dom,
    on,
    JSON,
    topic,
    xhr,
    script,
    request,
    all,
    Deferred,
    cookie,
    parser,
  
    registry,
    Button,
    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    template
) {
    return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        map: null,
        baseClass: null,
        templateString: template,
        constructor: function(config) {
            console.log("widgets._eDock.drawToolbar::constructor", arguments);
            declare.safeMixin(this, config);
            this.inherited(arguments);
        },

        postCreate: function() {
            console.log("widgets._eDock.drawToolbar::postCreate", arguments);
            var self = this;
            parser.parse();
            var grid_layer;

             // obtain the grid layer from the map
            var layers = self.map.graphicsLayerIds;
            var lyrs = Array.filter(layers, function(id) {
                var lyr = self.map.getLayer(id);
                try {
                    var result = lyr.name.indexOf("Grid") > -1;
                    return result;
                } catch (e) {
                    return false;
                }
            });

            if (lyrs.length > 1) {
                console.log("More then one grid layer exists in the map");
            } else if (lyrs.length === 0) {
                console.log("There were no grid layers found in the map");
            } else {
                grid_layer = self.grid_layer = lyrs[0];
            }

            var draw_bar = self.draw_bar = new Draw(self.map, {
                showTooltips: true,
                drawTime: 25,
                tolerance: 4
            });
            draw_bar.on("draw-complete", addToMap);

            // Add the control buttons to the template
            Array.forEach(["Point", "Multi Point", "Polygon", "Freehand Polygon", "Ellipse"], function(e) {
                var btn = new Button({
                    label: e,
                    // TODO-bind this function to the widget scope
                    onClick: function() {
                        self.map.graphics.clear();
                        var grid = self.map.getLayer(grid_layer);
                        grid.hide();
                        grid.clearSelection();
                        grid.setDefinitionExpression("");
                        grid.refresh();

                        var grid_search_list = dom.byId('id_grid_cells');
                        var grid_update_list = dom.byId('id_edit_grid_cells');
                        grid_search_list.value = "";
                        grid_update_list.value = "";

                        var tool = this.label.toUpperCase().replace(/ /g, "_");
                        self.map.hideZoomSlider();
                        self.map.setInfoWindowOnClick(false);
                        draw_bar.activate(Draw[tool]);
                    }
                }, self[e]);
            });

            function addToMap(evt) {
                var symbol;
                draw_bar.deactivate();
                self.map.showZoomSlider();
                self.map.setInfoWindowOnClick(true);
                self.map.graphics.clear();
                switch (evt.geometry.type) {
                    case "point":
                        symbol = new SimpleMarkerSymbol();
                        break;
                    case "multipoint":
                        symbol = new SimpleMarkerSymbol();
                        break;
                    case "polyline":
                        symbol = new SimpleLineSymbol();
                        break;
                    default:
                        symbol = new SimpleFillSymbol();
                        break;
                  }
                var graphic = new Graphic(evt.geometry, symbol);
                self.map.graphics.add(graphic);
                self.query_grid(graphic);
            }
        },

        query_grid: function(graphic) {
            var self = this;
            var lyr = self.grid_layer;
            var layer = self.map.getLayer(lyr);

            if (layer.getDefinitionExpression()) {
                layer.clearSelection();
                layer.setDefinitionExpression("");               
                layer.refresh();
            }
            
            var query = new Query();
            query.geometry = graphic.geometry;
            layer.queryFeatures(query, function(featureSet) {
                console.log(featureSet);
                var grid_search_list = dom.byId('id_grid_cells');
                var grid_update_list = dom.byId('id_edit_grid_cells');
                // var grid_list = registry.byId("_gridList");
                // clear all html from the grid list content node
                // grid_list.clearSelection();

                var grid_cells = Array.map(featureSet.features, function(feature) {
                    var deferred = new Deferred();
                    var grid_cell = feature.attributes.GRID;
                    return deferred.resolve(grid_cell);
                });

                all(grid_cells).then(function(array) {
                    var selectionSymbol = new SimpleFillSymbol(
                        SimpleFillSymbol.STYLE_SOLID,
                         new SimpleLineSymbol(SimpleLineSymbol.STYLE_DASHDOT,
                            new Color([255, 0, 0]), 2),
                             new Color([255, 255, 0, 0.5]
                                )
                             );
                    layer.setSelectionSymbol(selectionSymbol);
                    // sort the array in alpha numerical order
                    array.sort();
                    grid_search_list.value = array;
                    grid_update_list.value = array;

                    // grid_list.on('dgrid-select', function(event) {
                    //     var rows = event.rows;
                    //     var cells = [];
                    //     Array.forEach(rows, function(item) {
                    //         var cell = item.data;
                    //         cells.push(cell);
                    //     });
                    //     var exp = "GRID IN ('"+cells.join("', '") + "')";
                    //     var query = new Query();
                    //     query.where = exp;
                    //     layer.selectFeatures(query, FeatureLayer.SELECTION_ADD, function(e) {
                    //         console.log(e);
                    //         layer.redraw();
                    //     });
                    // });

                    // grid_list.on('dgrid-deselect', function(event) {
                    //     var rows = event.rows;
                    //     var cells = [];
                    //     Array.forEach(rows, function(item) {
                    //         var cell = item.data;
                    //         cells.push(cell);
                    //     });
                    //
                    //     var exp = "GRID IN ('"+cells.join("', '") + "')";
                    //     var query = new Query();
                    //     query.where = exp;
                    //     layer.selectFeatures(query, FeatureLayer.SELECTION_SUBTRACT, function(e) {
                    //         console.log(e);
                    //         layer.redraw();
                    //     });
                    // });

                    
                    var defExp = "GRID IN ('"+ array.join("', '") + "')";                    
                    layer.setDefinitionExpression(defExp);

                    layer.show();
                    layer.refresh();

                    var query = new Query();
                    query.where = defExp;
                    layer.selectFeatures(query, FeatureLayer.SELECTION_NEW, function(e) {
                        console.log(e);
                    });
                });
            });
        }
    });
});