module.exports = function(grunt) {
  grunt.initConfig({

    watch: {
      configFiles: {
          files: ['gruntfile.js'],
          options: {
            'reload': true
          }
      },
      main: {
        cwd: '.',
        files: [
          'rtaa_gis/fileApp/static/**/*.js',
        ],
        tasks: [
          'jshint'
        ],
        options: {
          'spawn': false,
          'atBegin': true
        }
      }
    },
    jshint : {
      options: {
        reporter: require('jshint-stylish'),
        curly: true,
        eqeqeq: true,
        eqnull: true,
        browser: true,
        dojo: true,
        esversion: 6
      },

      all: [
        'gruntfile.js',
        'rtaa_gis/fileApp/static/fileApp/**/*.js',
        '!rtaa_gis/fileApp/static/fileApp/pdfjs/**/*.js',
        'tests/**/*.js'
      ]
    },
    connect: {
      options: {
          livereload: false,
          port: 3003,
          protocol: 'http'
      },
      main: {
        options: {
            base: './',
            open: {
                target: 'http://localhost:3003/node_modules/intern/index.html'
            }
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-jshint');

  grunt.registerTask('default', [
    'jshint',
    'connect',
    'watch'
  ]);
};
