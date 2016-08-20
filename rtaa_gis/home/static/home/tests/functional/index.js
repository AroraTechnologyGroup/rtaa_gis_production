// in tests/functional/index.js
define([
  'intern!object',
  'intern/chai!assert',
  '../support/elements/router_test.js'
], function (registerSuite, assert, RouterTest) {
  registerSuite(function () {
    var router_test;
    return {
      // on setup, we create an IndexPage instance
      // that we will use for all the tests
      setup: function () {
        router_test= new RouterTest(this.remote);
      },

      'TopNavLinks': function() {
        return router_test
          .top_nav()
          .then(function (result) {
            assert.isTrue(result,
              'Main navigation links should change url to correct page');
          });
      }
    };
  });
});
