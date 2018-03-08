define([
  "dojo/Deferred",
  "dojo/_base/lang",
  "dojo/_base/array",
  'dojo/_base/unload',
  "dojo/_base/declare",
  "dojo/request",
  "dojo/mouse",
  "dojo/parser",
  "dojo/cookie",
  "dojo/json",
  "dojo/hash",
  "dojo/query",
  "dojo/topic",
  "dojo/dom-class",
  "dojo/dom-style",
  "dojo/dom-attr",
  "dojo/dom-construct",
  "dojo/dom",
  "dojo/on",

  "esri/geometry/Point",
  "esri/SpatialReference",

  'dijit/registry',
  "dijit/Menu",
  "dijit/popup",
  "dijit/MenuItem",
  "dijit/_WidgetBase",

  "dojo/NodeList-traverse",
    ],
    function (
      Deferred,
      lang,
      Array,
      baseUnload,
      declare,
      request,
      mouse,
      parser,
      cookie,
      JSON,
      hash,
      query,
      topic,
      domClass,
      domStyle,
      domAttr,
      domConstruct,
      dom,
      on,

      Point,
      SpatialReference,

      registry,
      Menu,
      popup,
      MenuItem,
      _WidgetBase
  ) {

      var panel_btn = dom.byId('_file_type_handle');
      var panel_btn2 = dom.byId('_doc_type_handle');
      var panel_btn3 = dom.byId('_map_handle');
      var panel_btn4 = dom.byId('_edit_handle');
      var panel_btn5 = dom.byId('_batch_edit_handle');

      var slider_panel = dom.byId('_slider_panel');

      var file_type_html = dom.byId('_file_type_group');
      var doc_type_html = dom.byId('_doc_type_group');
      var map_html = dom.byId('_map_group');

      var _container = dom.byId('_container');
      var update_panel = dom.byId('_update_panel');

      var ftype_all = dom.byId('all_file_type_select_all');

      var doctype_all = dom.byId('_doc_type_select_all');

      var edit_disc_all = query('#id_edit_discipline input[value="all"]');
      var edit_sheet_all = query('#id_edit_sheet_type input[value="all"]');
      var edit_doc_all = query('#id_edit_doc_type input[value="all"]');

      var grid_search_list = dom.byId('id_grid_cells');
      var grid_update_list = dom.byId('id_edit_new_grid_cells');

      // add the DRF class names to the django fieldWrapper to get the calendar
      Array.forEach(query('.fieldWrapper'), function (e) {
        // domClass.add(e, 'form-group');
      });

      Array.forEach(query('.fieldWrapper input'), function (e) {
        // domClass.add(e, 'form-control');
      });

      // make the multi-select boxes side by side
      Array.forEach(query('.fieldWrapper > select').parent(), function (e) {
        // domClass.add(e, 'inline');
      });

      Array.forEach(query('.fieldWrapper > ul').parent(), function (e) {
        // domClass.add(e, 'inline-list');
      });

      var btn_accrd = query('button.accordion');
      var icons = query('.fileIcon');
      var f_nodes = query('#id_file_type input');
      var d_nodes = query('#id_image_type input');
      var t_nodes = query('#id_table_type input');
      var gis_nodes = query('#id_gis_type input');
      var doc_nodes = query('#id_document_type input');
      var edit_disc_nodes = query('#id_edit_discipline input');
      var edit_sheet_nodes = query('#id_edit_sheet_type input');
      var edit_doc_nodes = query('#id_edit_doc_type input');

      return declare("App", [_WidgetBase], {
        map: null,
        constructor: function() {
          this.inherited(arguments);
        },
        postCreate: function () {
          this.inherited(arguments);
          var self = this;
          var view_menu = self.view_menu = new Menu({
            targetNodeIds: ["_resultBox"],
            selector: ".fileIcon.viewable"
          });

          var non_view_menu = self.non_view_menu = new Menu({
            targetNodeIds: ["_resultBox"],
            selector: ".fileIcon.non-viewable"
          });

          var download_menu_item = function () {
            return new MenuItem({
              label: "Download",
              iconClass: "taskIcon",
              onClick: function (evt) {
                var node = this.getParent().currentTarget;
                var _id = domAttr.get(node, "data-file-id");

                // if not on the local server get the SCRIPT NAME
                var url;
                if (window.location.hostname !== '127.0.0.1') {
                  var script_name = window.location.pathname.split("/")[1];
                  url = window.location.origin + "/" + script_name + "/fileApp/eng-io/" + _id + "/_download/";
                } else {
                  url = window.location.origin + "/fileApp/eng-io/" + _id + "/_download/";
                }
                var a = domConstruct.create("a", {
                  href: url,
                  download: true,
                  withCredentials: true
                });
                // the anchor node has to be added to the dom before the domEvent can be fired
                domConstruct.place(a, "_resultBox");
                a.click();
                domConstruct.destroy(a);
                console.log(_id);
              }
            });
          };

          var view_menu_item = function () {
            return new MenuItem({
              label: "View File",
              onClick: function (evt) {
                var node = this.getParent().currentTarget;
                var _id = domAttr.get(node, "data-file-id");
                // if not on the local server get the SCRIPT NAME
                var url;
                if (window.location.hostname !== '127.0.0.1') {
                  var script_name = window.location.pathname.split("/")[1];
                  url = window.location.origin + "/" + script_name + "/fileApp/eng-io/" + _id + "/_view/";
                } else {
                  url = window.location.origin + "/fileApp/eng-io/" + _id + "/_view";
                }

                var a = domConstruct.create("a", {
                  href: url,
                  target: "_blank",
                  withCredentials: true
                });
                // the anchor node has to be added to the dom before the domEvent can be fired
                domConstruct.place(a, "_resultBox");
                a.click();
                domConstruct.destroy(a);
              }
            });
          };

          view_menu.addChild(download_menu_item());
          view_menu.addChild(view_menu_item());

          // cloning the Menu Item allows it to be reused
          non_view_menu.addChild(download_menu_item());

          view_menu.startup();
          non_view_menu.startup();


          self.setupConnections();
        },

        setupConnections: function() {
          var self = this;
          // disable the click event for the dropdown buttons in the update panel
          if (btn_accrd) {
            Array.forEach(btn_accrd, function (e) {
              on(e, 'click', function (evt) {
                evt.preventDefault();
                domClass.toggle(e, "active");
                var panel = e.nextElementSibling;
                if (domClass.contains(panel, "active")) {
                  domClass.replace(panel, "off", "active");
                } else {
                  domClass.replace(panel, "active", "off");
                }
              });
            });
          }

          if (panel_btn) {
            on(panel_btn, 'click', function (event) {
              event.preventDefault();
              self.checkPanel(event).then(function (e) {
                domClass.remove(doc_type_html, "visible");
                domClass.remove(map_html, "visible");
                domClass.toggle(file_type_html, "visible");
              });
            });
          }

          if (panel_btn2) {
            on(panel_btn2, 'click', function (event) {
              event.preventDefault();
              self.checkPanel(event).then(function (e) {
                domClass.remove(file_type_html, "visible");
                domClass.remove(map_html, "visible");
                domClass.toggle(doc_type_html, "visible");
              });
            });
          }

          if (panel_btn3) {
            on(panel_btn3, 'click', function (event) {
              event.preventDefault();
              self.checkPanel(event).then(function (e) {
                domClass.remove(doc_type_html, "visible");
                domClass.remove(file_type_html, "visible");

                domClass.toggle(map_html, "visible");
              });
            });
          }

          if (panel_btn4) {
            on(panel_btn4, 'click', function (event) {
              event.preventDefault();
              // if the map button is active, click it to close the map
              if (!domClass.contains(panel_btn3, "btn-clear")) {
                on.emit(panel_btn3, "click", {
                  "bubbles": false
                });
              }


              domClass.toggle(panel_btn4, 'btn-clear');

              if (domClass.contains(update_panel, 'close')) {
                domClass.replace(update_panel, 'open', 'close');
                domClass.replace(_container, 'ropen', 'rclose');
              } else if (domClass.contains(update_panel, 'open')) {
                domClass.replace(update_panel, 'close', 'open');
                domClass.replace(_container, 'rclose', 'ropen');
              } else {
                domClass.add(update_panel, 'open');
                domClass.add(_container, 'ropen');
              }

            });
          }

          if (panel_btn5) {
            on(panel_btn5, 'click', function(event) {
                event.preventDefault();
            });
          }

          if (icons) {
            Array.forEach(icons, function (div) {
              on(div, 'click', function (evt) {
                console.log(evt);
                // close the context menu
                Array.forEach([self.view_menu, self.non_view_menu], function (e) {
                  popup.close(e);
                });
                // get all data-atts on the icon and place data in the update form
                var file_id = domAttr.get(div, 'data-file-id');
                var date_added = domAttr.get(div, 'data-file-date-added');
                var file_path = domAttr.get(div, 'data-file-path');
                var base_name = domAttr.get(div, 'data-file-base-name');
                var grid_cells = domAttr.get(div, 'data-file-grid-cells');
                var project_title = domAttr.get(div, 'data-file-project-title');
                var project_desc = domAttr.get(div, 'data-file-project-desc');
                var project_date = domAttr.get(div, 'data-file-project-date');
                var sheet_title = domAttr.get(div, 'data-file-sheet-title');
                var sheet_type = domAttr.get(div, 'data-file-sheet-type');
                var doc_type = domAttr.get(div, 'data-file-doc-type');
                var sheet_desc = domAttr.get(div, 'data-file-sheet-desc');
                var vendor = domAttr.get(div, 'data-file-vendor');
                var discipline = domAttr.get(div, 'data-file-discipline');
                var airport = domAttr.get(div, 'data-file-airport');
                var funding_type = domAttr.get(div, 'data-file-funding-type');
                var grant_number = domAttr.get(div, 'data-file-grant-number');

                if (mouse.isLeft(evt)) {
                  // populate the edit form with these values
                  if (!domClass.contains(update_panel, 'open')) {
                    on.emit(panel_btn4, "click", {
                      bubbles: true,
                      cancelable: true
                    });
                  }

                  dom.byId('id_edit_id').value = file_id;

                  dom.byId('id_edit_base_name').value = base_name;

                  // empty the div of grid cells
                  var edit_grid_list = dom.byId("id_edit_grid_cells");
                  domConstruct.empty(edit_grid_list);
                  // add checkbox and label for each grid cell
                  if (grid_cells) {
                    Array.forEach(grid_cells.split(","), function (e) {

                      var li = domConstruct.create("li");
                      var label = domConstruct.create("label", {"for": e + "_id", innerHTML: e});
                      var input = domConstruct.create("input", {
                        "type": "checkbox", "name": "edit_grid_cells", "value": e,
                        "id": e + "_id", "checked": true, "class": "form-control"
                      });

                      domConstruct.place(label, li);
                      domConstruct.place(input, label);
                      domConstruct.place(li, dom.byId("id_edit_grid_cells"));
                    });
                  } else {
                    domConstruct.place("<p>No Cells Assigned</p>", dom.byId("id_edit_grid_cells"));
                  }

                  if (sheet_title === "None") {
                    sheet_title = "";
                  }

                  dom.byId('id_edit_sheet_title').value = sheet_title;

                  Array.forEach(query("#id_edit_discipline input"), function (box) {
                    box.checked = false;
                  });
                  Array.forEach(discipline.split(","), function (e) {
                    Array.some(query("#id_edit_discipline input"), function (input) {
                      if (input.value === e) {
                        input.checked = true;
                      }
                    });
                  });
                  Array.forEach(query("#id_edit_sheet_type input"), function (box) {
                    box.checked = false;
                  });
                  Array.forEach(sheet_type.split(","), function (e) {
                    Array.some(query("#id_edit_sheet_type input"), function (input) {
                      if (input.value === e) {
                        input.checked = true;
                      }
                    });
                  });
                  Array.forEach(query("#id_edit_doc_type input"), function (box) {
                    box.checked = false;
                  });
                  Array.forEach(doc_type.split(","), function (e) {
                    Array.some(query("#id_edit_doc_type input"), function (input) {
                      if (input.value === e) {
                        input.checked = true;
                      }
                    });
                  });

                  if (project_title === "None") {
                    project_title = "";
                  }

                  dom.byId('id_edit_project_title').value = project_title;

                  if (project_desc === "None") {
                    project_desc = "";
                  }

                  dom.byId('id_edit_project_desc').value = project_desc;

                  if (project_date === "None") {
                    project_date = null;
                  }

                  dom.byId('id_edit_project_date').value = project_date;

                  if (sheet_desc === "None") {
                    sheet_desc = "";
                  }

                  dom.byId('id_edit_sheet_desc').value = sheet_desc;

                  if (vendor === "None") {
                    vendor = "";
                  }

                  dom.byId('id_edit_vendor').value = vendor;

                  if (funding_type === "None") {
                    funding_type = "";
                  }

                  dom.byId('id_edit_funding_type').value = funding_type;

                  Array.forEach(query("#id_edit_airport input"), function (e) {
                    if (e.value === airport) {
                      e.checked = true;
                    }
                  });

                  dom.byId('id_edit_date_added').value = date_added;

                  dom.byId('id_edit_file_path').value = file_path;

                  if (grant_number === "None") {
                    grant_number = "";
                  }

                  dom.byId('id_edit_grant_number').value = grant_number;
                }
              });
            });
          }

          if (ftype_all) {
            on(ftype_all, 'change', function(evt) {
              console.log(evt);
              evt.preventDefault();

              if (evt.target.checked) {
                // check all of the file type boxes
                Array.forEach([f_nodes, d_nodes, t_nodes, gis_nodes], function(d) {
                  Array.forEach(d, function (i) {
                    {
                      i.checked = true;
                    }
                  });
                });
              } else {
                // uncheck all of the file type boxes
                Array.forEach([f_nodes, d_nodes, t_nodes, gis_nodes], function(d) {
                  Array.forEach(d, function (i) {
                    {
                      i.checked = false;
                    }
                  });
                });
              }
            });
          }

          if (doctype_all) {
            on(doctype_all, 'change', function(evt) {
              console.log(evt);
              evt.preventDefault();

              if (evt.target.checked) {
                // check all of the file type boxes
                Array.forEach([doc_nodes], function(d) {
                  Array.forEach(d, function (i) {
                    {
                      i.checked = true;
                    }
                  });
                });
              } else {
                // uncheck all of the file type boxes
                Array.forEach([doc_nodes], function(d) {
                  Array.forEach(d, function (i) {
                    {
                      i.checked = false;
                    }
                  });
                });
              }
            });
          }

          if (edit_disc_all) {
            on(edit_disc_all, 'change', function(evt) {
              console.log(evt);
              evt.preventDefault();

              if (evt.target.checked) {
                // check all of the file type boxes
                Array.forEach([edit_disc_nodes], function(d) {
                  Array.forEach(d, function (i) {
                    {
                      i.checked = true;
                    }
                  });
                });
              } else {
                // uncheck all of the file type boxes
                Array.forEach([edit_disc_nodes], function(d) {
                  Array.forEach(d, function (i) {
                    {
                      i.checked = false;
                    }
                  });
                });
              }
            });
          }

          if (edit_sheet_all) {
            on(edit_sheet_all, 'change', function(evt) {
              console.log(evt);
              evt.preventDefault();

              if (evt.target.checked) {
                // check all of the file type boxes
                Array.forEach([edit_sheet_nodes], function(d) {
                  Array.forEach(d, function (i) {
                    {
                      i.checked = true;
                    }
                  });
                });
              } else {
                // uncheck all of the file type boxes
                Array.forEach([edit_sheet_nodes], function(d) {
                  Array.forEach(d, function (i) {
                    {
                      i.checked = false;
                    }
                  });
                });
              }
            });
          }

          if (edit_doc_all) {
            on(edit_doc_all, 'change', function(evt) {
              console.log(evt);
              evt.preventDefault();

              if (evt.target.checked) {
                // check all of the file type boxes
                Array.forEach([edit_doc_nodes], function(d) {
                  Array.forEach(d, function (i) {
                    {
                      i.checked = true;
                    }
                  });
                });
              } else {
                // uncheck all of the file type boxes
                Array.forEach([edit_doc_nodes], function(d) {
                  Array.forEach(d, function (i) {
                    {
                      i.checked = false;
                    }
                  });
                });
              }
            });
          }
          // remove the selected grids from the search and edit windows
          self.clearGrid = topic.subscribe("grids/clear", function() {
            if (grid_search_list) {
              grid_search_list.value = "";
            }
            // remove all of the html from the UpdateList
            if (grid_update_list) {
              domConstruct.empty(grid_update_list);
            }
          });
        },

        checkPanel: function (event) {

            var deferred = new Deferred();
            var target = event.target;
            // if the slider panel is not open, open it.
            if (!domClass.contains(slider_panel, "open") && !domClass.contains(slider_panel, "open_from_trans") && !domClass.contains(slider_panel, "close_to_trans")) {
              domClass.replace(slider_panel, "open", "close");

              // if the target button is for map, add then set the map class
              if (target === panel_btn3) {
                domClass.replace(slider_panel, "open_from_trans", "close_map");
              }
              domClass.remove(slider_panel, "close_map");
              domClass.remove(event.target, 'btn-clear');
              deferred.resolve(slider_panel);
            } else {
              // the panel is already open; if the button is not clear, close the panel, and make button clear.
              console.log(event.target);
              if (!domClass.contains(event.target, 'btn-clear')) {
                domClass.replace(slider_panel, "close", "open");
                domClass.replace(slider_panel, "close", "close_to_trans");
                // if the target button is for map, add the close map class
                if (event.target === panel_btn3) {
                  domClass.replace(slider_panel, "close_map", "open_map");
                  domClass.replace(slider_panel, "close_map", "open_from_trans");
                }
                domClass.add(event.target, 'btn-clear');
              } else {
                // the panel is open and the button is clear, keep the panel open, make other buttons clear
                // make this button blue
                Array.forEach([panel_btn, panel_btn2, panel_btn3], function (btn) {
                  if (btn !== target) {
                    domClass.add(btn, 'btn-clear');
                  }
                });

                if (panel_btn === target || panel_btn2 === target) {
                  // one of the file type buttons was clicked and the slider panel needs to move to this location
                  // from either the closed position or the open_map position.
                  if (domClass.contains(slider_panel, 'open_map')) {
                    // the map is open to 100%
                    // move it to the width of the file type panels
                    domClass.replace(slider_panel, 'close_to_trans', 'open_map');

                  } else if (domClass.contains(slider_panel, 'open_from_trans')) {
                    domClass.replace(slider_panel, 'close_to_trans', 'open_from_trans');
                  }
                } else if (panel_btn3 === target) {
                  // open the slider panel to the full extent from the file_type width
                  if (domClass.contains(slider_panel, 'open') || domClass.contains(slider_panel, 'close_to_trans')) {
                    domClass.replace(slider_panel, 'open_from_trans', 'open');
                    domClass.replace(slider_panel, 'open_from_trans', 'close_to_trans');
                  }
                }
                domClass.remove(event.target, 'btn-clear');
              }
              deferred.resolve(slider_panel);
            }

            return deferred.promise;
          }
      });
    });










