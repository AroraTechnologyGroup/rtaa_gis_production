require(["dojo/Deferred", "dojo/_base/array", 'dijit/registry', 'dojo/_base/unload', "dojo/hash", "dojo/query", "dojo/dom-class", "dojo/dom-construct", "dojo/dom", "dojo/on", 'dojo/domReady!'],
        function (Deferred, Array, registry, baseUnload, hash, query, domClass, domConstruct, dom, on) {

            var unLoad = function() {
                Array.forEach(registry.toArray(), function(item) {
                    item.destroyRecursive();
                });
            };
            baseUnload.addOnUnload(unLoad);

            var request_hash = hash();
            if (request_hash) {
                hash(request_hash);
            } else {
                hash("home");
            }
            // disable the loader gif
            var node = query(".loader")[0];
            domClass.remove(node, 'is-active');

            var footer_links = query("footer li");
            Array.forEach(footer_links, function (e) {
                domClass.add(e, "font-size--3");
            });

            var panel_btn = dom.byId('_file_type_handle');
            var panel_btn2 = dom.byId('_doc_type_handle');
            var panel_btn3 = dom.byId('_map_handle');
            var panel_btn4 = dom.byId('_reset_handle');
            var panel_btn5 = dom.byId('_edit_handle');

            var slider_panel = dom.byId('_slider_panel');

            var file_type_html = dom.byId('_file_type_group');
            var doc_type_html = dom.byId('_doc_type_group');
            var grid_cell_html = dom.byId('_grid_group');

            var _container = dom.byId('_container');
            var update_panel = dom.byId('_update_panel');

            var check_panel = function(event) {

                var deferred = new Deferred();
                // if the slider panel is not open, open it.
                 if (!domClass.contains(slider_panel, "open")) {
                    domClass.replace(slider_panel, "open", "close");
                    domClass.remove(event.target, 'btn-clear');
                    deferred.resolve(slider_panel);
                } else {
                     // the panel is already open; if the button is not clear, close the panel, and make button clear.
                     console.log(event.target);
                     if (!domClass.contains(event.target, 'btn-clear')) {
                         domClass.replace(slider_panel, "close", "open");
                         domClass.add(event.target, 'btn-clear');
                     } else {
                         // the panel is open and the button is clear, keep the panel open, make other buttons clear
                         // make this button blue
                         Array.forEach([panel_btn, panel_btn2, panel_btn3], function(btn) {
                             if (btn !== event.target) {
                                 domClass.add(btn, 'btn-clear');
                             }
                         });
                         domClass.remove(event.target, 'btn-clear');
                     }
                     deferred.resolve(slider_panel);
                 }

                return deferred.promise;
            };

            on(panel_btn, 'click', function(event) {
                event.preventDefault();
                check_panel(event).then(function(e) {
                    domClass.remove(doc_type_html, "visible");
                    domClass.remove(grid_cell_html, "visible");
                    domClass.toggle(file_type_html, "visible");
                });
            });

            on(panel_btn2, 'click', function(event) {
                event.preventDefault();
                check_panel(event).then(function(e) {
                    domClass.remove(file_type_html, "visible");
                    domClass.remove(grid_cell_html, "visible");
                    domClass.toggle(doc_type_html, "visible");
                });
            });

            on(panel_btn3, 'click', function(event) {
                event.preventDefault();
                check_panel(event).then(function(e) {
                    domClass.remove(doc_type_html, "visible");
                    domClass.remove(file_type_html, "visible");
                    domClass.toggle(grid_cell_html, "visible");
                });
            });

            on(panel_btn5, 'click', function(event) {
                event.preventDefault();
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
        });