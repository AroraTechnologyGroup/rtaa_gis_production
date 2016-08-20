define([
  'intern!bdd',
  'intern/chai!expect',
  'dijit/registry',
  "dojo/_base/array",
  'app/HomepageBanner'
], function(bdd, expect, registry, Array, HomepageBanner) {

  bdd.describe('the HomepageBanner Widget', function() {

    var homepage_banner;

    var destroy = function (widget) {
        Array.forEach(registry.toArray(), function(e) {
            registry.remove(e.id);
        });
    };

    bdd.beforeEach(function () {
      homepage_banner = new HomepageBanner();
    });

    bdd.afterEach(function () {
      destroy(homepage_banner);
    });

    bdd.it('should be a Homepage Banner', function() {
      expect(homepage_banner).to.be.an.instanceof(HomepageBanner);
    });
  });
});
