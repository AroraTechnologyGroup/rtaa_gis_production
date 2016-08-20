define([
  'intern!bdd',
  'intern/chai!expect',
  'dijit/registry',
  'dojo/_base/array',
  'app/PageBanner'
], function(bdd, expect, registry, Array, PageBanner) {

  bdd.describe('the PageBanner Widget', function() {

    var destroy = function (widget) {
        Array.forEach(registry.toArray(), function(e) {
            registry.remove(e.id);
        });
    };

    var page_banner;

    bdd.beforeEach(function () {
      page_banner = new PageBanner();
    });

    bdd.afterEach(function () {
      destroy(page_banner);
    });

    bdd.it('should be a PageBanner', function() {
      expect(page_banner).to.be.an.instanceof(PageBanner);
    });
  });
});
