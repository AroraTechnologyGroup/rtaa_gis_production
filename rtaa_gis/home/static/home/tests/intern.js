define({
	
	proxyPort: 9000,
//
//	// A fully qualified URL to the Intern proxy
	proxyUrl: 'http://localhost:9000/',

	capabilities: {
		'browserstack.selenium_version': '2.45.0'
	},
    runnerClientReporter: {
        id: 'WebDriver',
				writeHTML: 'true'
    },

	environments: [

		{ browserName: 'chrome', version: '39', platform: [ 'WINDOWS', 'MAC' ] }

	],

	// Maximum number of simultaneous integration tests that should be executed on the remote WebDriver service
	maxConcurrency: Infinity,

	loaders: {
			'host-node': 'dojo/dojo',
			"host-browser": "src/dojo/dojo.js",
	},


	loaderOptions: {
		// Packages that should be registered with the loader in each testing environment


		packages: [ {
            name: 'dgrid',
            location: 'src/dgrid'
          }, {
            name: 'dstore',
            location: 'src/dstore'
          }, {
            name: 'dijit',
            location: 'src/dijit'
          }, {
            name: 'esri',
            location: 'src/esri'
          }, {
            name: 'dojo',
            location: 'src/dojo'
          }, {
            name: 'dojox',
            location: 'src/dojox'
          }, {
            name: 'put-selector',
            location: 'src/put-selector'
          }, {
            name: 'util',
            location: 'src/util'
          }, {
            name: 'xstyle',
            location: 'src/xstyle'
          }, {
            name: 'app',
            location: 'src/app'
          }, {
            name: 'tests',
            location: 'tests'
          }, {
              name: 'moment',
              location: 'src/moment'
          }
                  ]
	},


	// Non-functional test suite(s) to run in each browser
	suites: ['tests/unit/all'],

	// Functional test suite(s) to execute against each browser once non-functional tests are completed

	// functionalSuites: ['tests/functional/index'],

	// A regular expression matching URLs to files that should not be included in code coverage analysis
	excludeInstrumentation: /^(?:tests|node_modules|bower_components|src\/(?:dgrid|dijit|dojo|dojox|put-selector|xstyle))\//
});
