/**
 * Created by rhughes on 7/25/2016.
 */
require([
    'dojo/dom',
    'dojo/dom-construct',
    'dojo/dom-class',
    'dojo/query',

    'dojo/domReady!'
], function(dom, domConstruct, domClass, query) {

    var first_button = query('.tab-title:first-of-type');
    var result = domClass.add(first_button[0], "is-active");
    var first_article = query('.tab-section:first-of-type');
    var result2 = domClass.add(first_article[0], "is-active");


});