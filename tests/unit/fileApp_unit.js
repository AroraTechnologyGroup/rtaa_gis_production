define([
  "fileApp/widgets/App",
  "dojo/dom-construct",
  "esri/map"

], function(
  App,
  domConstruct,
  Map
) {

  const { assert } = intern.getPlugin('chai');
  const { registerSuite } = intern.getInterface('object');

  registerSuite('fileApp', () => {
    var map;
    var node;
    var mapdiv;
    var widget;
    return {
      before() {
        node = domConstruct.create("div", { "id": "_resultBox" });
        domConstruct.place(node, window.document.body);
        mapdiv = domConstruct.create("div", {"id": "map"});
        domConstruct.place(node, window.document.body);
      },
      after() {
        if (node) {
          domConstruct.destroy(node);
        }

        if (mapdiv) {
          domConstruct.destroy(mapdiv);
        }
      },
      beforeEach() {

        map = new Map(mapdiv);
        widget = new App();
      },
      afterEach() {
        widget.destroy();
        widget = null;
        map.destroy();
        map = null;

      },
      tests: {
        'create new'() {
          assert.doesNotThrow(() => new App());
        }
      }
    };
  });
});