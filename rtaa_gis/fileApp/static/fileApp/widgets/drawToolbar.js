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
    "dojo/dom-class",
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
    "dojo/query",
    
    "dijit/registry",
    "dijit/ConfirmDialog",
    "dijit/form/Button",
    "dijit/form/CheckBox",
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
    domClass,
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
    query,
  
    registry,
    ConfirmDialog,
    Button,
    CheckBox,
    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    template
) {
    return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        map: null,
        baseClass: "_draw-bar",
        templateString: template,
        optOut: false,
        grid_layer: null,

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

            var cellDialog = self.cellDialog = new ConfirmDialog({
              title: "Grid Selection Next Steps",
              autofocus: false
            });

            var content = domConstruct.create("div", {"id": "_dialogBox"});

            var auth_node = dom.byId("_auth_panel");
            var edit_lvl = Array.some(query("._auth_group", auth_node), function(e) {
              if (e.innerHTML.trim() === "_RTAA Planning and Engineering") {
                return true;
              } else {
                return false;
              }
            });

            var text = "<p><b>SEARCH</b> - To locate files that have been assigned to these cells, click the blue Search button.</p>\
                <ul><li>The selected grid cells have been added to the 'Grid Cells:' text input.</li></ul>";

            if (edit_lvl) {
              text += "<p></p><b>UPDATE</b> - To assign the grid cell(s) to a file, click the Attributes button.</p>\
              <ul><li>This will open the Attribute panel.</li>\
              <li>The grid cells have been added into the 'New Grid Cells:' input of the Attribute Panel.</li>\
              <li>If the File Name input is empty, then a file is not selected.</li>\
                <ul><li>Click the Map button to close the map.</li>\
                <li>Click on the desired file in the file browser window to select it.</li>\
                <li>Currently only one file can be selected and updated at a time.</li></ul>\
              <li>Clicking Save in the Attribute panel will assign the grid cell(s) to the selected file.</li></ul>";
            }

            text +=  "<input id='dialogOptOut' name='dialogOptOut' data-dojo-type='dijit/form/CheckBox' value='optOut'/>\
            <label for='dialogOptOut'>Do not show this dialog again</label>";

            var message_div = domConstruct.create("div", {"class": "menu-panel"});

            domConstruct.place(domConstruct.toDom(text), message_div);
            domConstruct.place(message_div, content);

            self.cellDialog.set("content", content);

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
                console.log("More than one grid layer exists in the map");
            } else if (lyrs.length === 0) {
                console.log("There were no grid layers found in the map");
            } else {
                grid_layer = self.grid_layer = self.map.getLayer(lyrs[0]);
            }

            var draw_bar = self.draw_bar = new Draw(self.map, {
                showTooltips: true,
                drawTime: 25,
                tolerance: 4
            });
            draw_bar.on("draw-complete", addToMap);

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
                // the query grid function will populate the Search and Edit windows with the selected Grid Cell values
                self.query_grid(graphic).then(function(featureSet) {
                  self.updateGridInputs(featureSet);
                  self.renderSelection(featureSet);
                  // if the user has not opted out, show the dialog
                  if (!self.optOut) {
                    self.cellDialog.show();
                  }
                });
            }
            self.setupConnections();
        },

        setupConnections: function() {
          var self = this;
          var okButton = self.cellDialog.okButton;
          var cancelButton = self.cellDialog.cancelButton;
          var optOut = registry.byId('dialogOptOut');
          var select_btn = self.Select;
          var draw_bar = self.draw_bar;

          if (okButton) {
            on(okButton, 'click', function (evt) {
              if (optOut.checked) {
                self.optOut = true;
              } else {
                self.optOut = false;
              }
            });
          }

          if (cancelButton) {
            on(cancelButton, 'click', lang.hitch(self, function (evt) {
              optOut.set('checked', false);
            }));
          }

          if (select_btn) {
            on(select_btn, 'click', function (evt) {
              window.calcite.stopPropagation(evt);
              window.calcite.bus.emit('dropdown:toggle', {
                node: self._dropdown
              });
            });
          }

          if (window.calcite) {
            window.calcite.bus.on('dropdown:toggle', function (options) {
              console.log(options.node);
              // this is needed to override the css rules for dropdown ??bug??
              domClass.toggle(self._menu, "display", null);
            });
          }

          // Add the events to the draw buttons
          Array.forEach(["Point", "Multi Point", "Polygon", "Freehand Polygon", "Ellipse", "Circle"], function(e) {
            var node = self[e];
            on(node, 'click', function(evt) {
              evt.preventDefault();
              self.map.graphics.clear();
              var grid = self.grid_layer;
              grid.clearSelection();
              grid.setDefinitionExpression("");
              grid.refresh();

              var tool = e.toUpperCase().replace(/ /g, "_");
              self.map.hideZoomSlider();
              self.map.setInfoWindowOnClick(false);
              draw_bar.activate(Draw[tool]);
            });
          });

          var clear_btn = self.ClearAll;
          on(clear_btn, 'click', function(evt) {
            evt.preventDefault();
            self.map.graphics.clear();
            var layer = self.grid_layer;
            if (layer.getDefinitionExpression()) {
                layer.clearSelection();
                layer.setDefinitionExpression("");
                layer.refresh();
            }
            topic.publish("grids/clear");
          });
        },

        query_grid: function(graphic) {
          var self = this;
          var layer = self.grid_layer;
          var main_deferred = new Deferred();
          // if (layer.getDefinitionExpression()) {
          //     layer.clearSelection();
          //     layer.setDefinitionExpression("");
          //     layer.refresh();
          // }

          var query = new Query();
          query.geometry = graphic.geometry;
          layer.queryFeatures(query, function (featureSet) {
            console.log(featureSet);
            var grid_cells = Array.map(featureSet.features, function (feature) {
              var deferred = new Deferred();
              var grid_cell = feature.attributes.GRID;
              deferred.resolve(grid_cell);
              return deferred.promise;
            });

            all(grid_cells).then(function (array) {
              main_deferred.resolve(array);
            });
          });

          return main_deferred.promise;
        },

        updateGridInputs: function(array) {
          var self = this;
          var grid_search_list = dom.byId('id_grid_cells');
          var grid_update_list = dom.byId('id_edit_new_grid_cells');
          var layer = self.grid_layer;
          array.sort();
          // update the Search Text box with grid values
          grid_search_list.value = array;
          // add the New Grid Cells to the update box as checkboxes
          Array.forEach(array, function(e) {

              var li = domConstruct.create("li");
              var label = domConstruct.create("label", {"for" : e+"_id", innerHTML: e});
              var input = domConstruct.create("input", {"type": "checkbox", "name": "edit_new_grid_cells", "value": e,
                  "id": e+"_id", "checked": true, "class": "form-control"});
              on(input, "change", function(evt) {
                var query = new Query();
                var exp = "GRID = '"+evt.target.value+"'";
                query.where = exp;

                if (evt.target.checked) {
                  // add the cell to the definition query
                  layer.selectFeatures(query, FeatureLayer.SELECTION_ADD, function(e) {
                      console.log(e);
                      layer.redraw();
                  });
                } else {
                  // remove the cell from the definition query
                  layer.selectFeatures(query, FeatureLayer.SELECTION_SUBTRACT, function(e) {
                      console.log(e);
                      layer.redraw();
                  });
                }
              });

              domConstruct.place(label, li);
              domConstruct.place(input, label);
              domConstruct.place(li, grid_update_list);

          });
        },

        renderSelection: function(featureSet) {
          var self = this;
          var array = featureSet;
          var layer = self.grid_layer;
          var selectionSymbol = new SimpleFillSymbol(
            SimpleFillSymbol.STYLE_SOLID,
             new SimpleLineSymbol(SimpleLineSymbol.STYLE_DASHDOT,
                new Color([255, 0, 0]), 2),
                 new Color([255, 255, 0, 0.5])
                 );
          layer.setSelectionSymbol(selectionSymbol);
          // sort the array in alpha numerical order
          var defExp = "GRID IN ('"+ array.join("', '") + "')";
          layer.setDefinitionExpression(defExp);
          layer.show();
          layer.refresh();

          var query = new Query();
          query.where = defExp;
          // initially all the cells are selected using the same definition query as the def expression.
          // the checkboxes allow the user to toggle cell selection to uninclude them from the post data
          layer.selectFeatures(query, FeatureLayer.SELECTION_NEW, function(e) {
              console.log(e);
          });
        }
    });
});