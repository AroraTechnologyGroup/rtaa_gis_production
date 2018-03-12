require([
    "fileApp/widgets/App",
    "dojo/Deferred",
    "dojo/_base/lang",
    "dojo/request",
    "dojo/mouse",
    "fileApp/widgets/drawToolbar",
    "dojo/parser",
    "dojo/cookie",
    "dojo/json",
    "dojo/_base/array",
    'dijit/registry',
    'dojo/_base/unload',
    "dojo/hash",
    "dojo/query",
    "dojo/dom-class",
    "dojo/dom-style",
    "dojo/dom-attr",
    "dojo/dom-construct",
    "dojo/dom",
    "dojo/on",
    "esri/arcgis/utils",
    "esri/config",
    "esri/urlUtils",
    "dijit/Menu",
    "dijit/popup",
    "dijit/MenuItem",
    "dijit/layout/BorderContainer",
    "dijit/layout/ContentPane",
    "esri/IdentityManager",
    "dojo/NodeList-traverse",
    'dojo/domReady!'
    ], function (
        App,
        Deferred,
        lang,
        request,
        mouse,
        drawToolbar,
        parser,
        cookie,
        JSON,
        Array,
        registry,
        baseUnload,
        hash,
        query,
        domClass,
        domStyle,
        domAttr,
        domConstruct,
        dom,
        on,
        arcgisUtils,
        esriConfig,
        urlUtils,
        Menu,
        popup,
        MenuItem,
        BorderContainer,
        ContentPane,
        esriId
        ) {
            parser.parse();
            var map, cred = "esri_jsapi_id_manager_data";
            var deferred;

            Array.forEach(["https://tasks.arcgisonline.com", "http://tasks.arcgisonline.com"], function(url) {
                esriConfig.defaults.io.corsEnabledServers.push({
                    "host": url,
                    "withCredentials": true
                });
            });


            var proxyUrl;
            if (window.location.hostname === "gis.renoairport.net") {
                proxyUrl = "https://gis.renoairport.net/DotNet/proxy.ashx";
            } else {
                proxyUrl = "https://gisapps.aroraengineers.com/DotNet/proxy.ashx";
            }
            Array.forEach(["www.arcgis.com", "tiles.arcgis.com", "services6.arcgis.com"], function(url) {
                urlUtils.addProxyRule({
                    urlPrefix: url,
                    proxyUrl: proxyUrl
                });
            });

            esriConfig.defaults.io.alwaysUseProxy = false;


            function loadCredentials(){
                var idJson, idObject;

                if (supports_local_storage()) {
                    // read from local storage
                    idJson = window.localStorage.getItem(cred);
                }
                else {
                    // read from a cookie
                    idJson = cookie(cred);
                }

                if (idJson && idJson != "null" && idJson.length > 4) {
                    idObject = JSON.parse(idJson);
                    esriId.initialize(idObject);
                }
                else {
                    // console.log("didn't find anything to load :(");
                }
            }

            function storeCredentials(){
                // make sure there are some credentials to persist
                if (esriId.credentials.length === 0) {
                    return;
                }

                // serialize the ID manager state to a string
                var idString = JSON.stringify(esriId.toJson());
                // store it client side
                if (supports_local_storage()) {
                    // use local storage
                    window.localStorage.setItem(cred, idString);
                    // console.log("wrote to local storage");
                }
                else {
                    // use a cookie
                    cookie(cred, idString, {expires: 1});
                    // console.log("wrote a cookie :-/");
                }
            }

            function supports_local_storage(){
                try {
                    return "localStorage" in window && window.localStorage !== null;
                } catch (e) {
                    return false;
                }
            }

            var unLoad = function() {
                storeCredentials();
                Array.forEach(registry.toArray(), function(item) {
                    item.destroyRecursive();
                });
            };
            baseUnload.addOnUnload(unLoad);

            loadCredentials();

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

            // load the app
            var app = new App();

            var createMapOptions = {
                mapOptions: {
                    slider: false
                },
                usePopupManager: true,

                geometryServiceURL: "http://tasks.arcgisonline.com/ArcGIS/rest/services/Geometry/GeometryServer"
            };

            var webMapItemID = "579f89362fe244b0834cf67159b1e689";
            deferred = arcgisUtils.createMap(webMapItemID, 'map', createMapOptions);
            deferred.then(function(e) {
                map = e.map;
                app.set('map', map);

                var widget = new drawToolbar({
                  map: map,
                  id: "_draw_bar"
                }, "widgetNode");
                // widget.startup();

            });
        });