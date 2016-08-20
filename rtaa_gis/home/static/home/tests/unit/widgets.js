define([
  'intern!bdd',
  'intern/chai!expect',
  'dijit/registry',
  'app/Card',
  "dojo/_base/array",
], function(bdd, expect, registry, Card, HomepageBanner,
PageBanner, Array) {

  bdd.describe('widgets that make up the app', function() {
    var destroy = function (widget) {
        Array.forEach(registry.toArray(), function(e) {
            e.id.destoryRecursive();
        });
    };

    var card;

    bdd.describe('the Card Widget', function() {

      bdd.beforeEach(function () {
        var options = {
            baseClass: "",
            imgSrc: "",
            header: "",
            contents: ""
        };

        card = new Card(options, null);
      });

      bdd.afterEach(function () {
        destroy(card);
      });

      bdd.it('should be a card', function() {
        expect(card).to.be.an.instanceof(Card);
      });
    });
  });
});
