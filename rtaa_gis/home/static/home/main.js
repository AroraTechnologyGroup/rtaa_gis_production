/**
 * Created by rhughes on 7/26/2016.
 */
require(['dojo/parser', "dojo/query", "dojo/dom-class", 'dijit/layout/ContentPane', 'dojo/domReady!'],
    function (parser, query, domClass) {
        var node = query(".loader")[0];
        domClass.remove(node, 'is-active');

});