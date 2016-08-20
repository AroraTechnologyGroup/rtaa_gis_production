define([
  "dojo/_base/array",
  "dojo/Deferred",
  "dojo/promise/all"
], function (Array, Deferred, all) {
  // the page object is created as a constructor
  // so we can provide the remote Command object
  // at runtime
  function RouterTest(remote) {
    this.remote = remote;
  }

  RouterTest.prototype = {
    constructor: RouterTest,
    top_nav: function() {
      return this.remote
          .get(require.toUrl('index.html'))
          .setFindTimeout(5000)
          .findAllByClassName('top-nav-link')
          .then(function(arr) {
            var text_links = {
              "RTAA GIS": "",
              "GIS Portal": "GIS Portal",
               "Departments": "Departments",
               "Web Resources": "Web Resources",
               "Help": "Help"
            };
            var calls = Array.map(arr, function(e) {
              var deferred = new Deferred();
              var text = e.innerHTML;
              e.click()
              .getCurrentUrl().then(function(url) {
                console.log(url);
              });
            });
          });

      }
    };

    // …additional page interaction tasks

  return RouterTest;
});
