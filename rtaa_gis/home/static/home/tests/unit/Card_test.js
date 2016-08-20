define([
  'intern!bdd',
  'intern/chai!expect',
  'dijit/registry',
  'app/Card',
  'dojo/_base/Array',
  'dojo/Deferred',
  'dojo/promise/all'
], function(
  bdd,
  expect,
  registry,
  Card,
  Array,
  Deferred,
  all
) {

  bdd.describe('the Card Widget', function() {

    var destroy = function (widget) {
        Array.forEach(registry.toArray(), function(e) {
            registry.remove(e.id);
        });
    };

    var card;

    bdd.before(function() {
    });

    bdd.after(function() {
    });

    bdd.beforeEach(function () {
      card = new Card();
    });

    bdd.afterEach(function () {
      destroy(card);
    });

    bdd.it('should be a card', function() {
      expect(card).to.be.an.instanceof(Card);
    });
  });
});
