module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt, {pattern: 'grunt-contrib-*'});
    var path = require('path');


  grunt.initConfig({

    clean: {
      build: {
        src: ['dist/']
      },
      uncompressed: {
        src: [
          'dist/**/*.uncompressed.js'
        ]
      }
    },

    copy: {
        main: {
            files: [{
                expand: true,
                cwd: './src/',
                src: ['built.html'],
                dest: './dist/',
                rename: function (dest, src) {
                    return dest + 'index.html';
                }
            }]
        }
    },
    dojo: {
      dist: {
          options: {
              releaseDir: './dist'
          }
      },
      options: {
          profile: 'build.profile.js',
          dojo: './src/dojo/dojo.js',
          load: 'build',
          cwd: './',
          basePath: './src'
        }
    },

    watch: {
      main: {
        files: ['**/*.js', '**/*.html',
      '**/*.styl'],
        tasks: ['stylus:compile', 'jshint']
      }
    },

    stylus: {
      compile: {
        options: {
          compress: false,
          'import': [ 'nib']
        },
        use: [
          require('autoprefixer-stylus')
        ],
        files: [{
          './src/app/resources/app.css': [
            './src/app/resources/app.styl'
          ]
        }]
      }
    },

    jshint : {
      options: {
        reporter: require('jshint-stylish'),
        curly: true,
        eqeqeq: true,
        eqnull: true,
        browser: true,
        dojo: true
      },

      all: ['gruntfile.js', './src/app/**/*.js', './tests/**/*.js']
    },

    connect: {
			options: {
				port: 3000,
				hostname: 'localhost'
			},
      dev: {
        options: {
          base: './src',
          open: {
            target: 'http://localhost:3000/index.html'
          }
        }
      },
        test: {
            options: {
                base: '.',
              open: {
                target: 'http://localhost:3000/node_modules/intern/client.html?config=tests/intern'
              }
            }
        },
        dist: {
            options: {
                base: 'dist',
              open: {
                target: 'http://localhost:3000/index.html'
              }
            }
        }
    },

    intern: {
			local: {
				options: {
					runType: 'client',
					config: 'src/app/tests/intern'
				}
			},
			remote: {
				options: {
					runType: 'runner',
					config: 'src/app/tests/intern'
				}
			}
		}
  });

  grunt.registerTask('serve', function (target) {
		if (target === 'dist') {
			return grunt.task.run([
				'build',
				'connect:dist:keepalive'
			]);
		}

		grunt.task.run([
			'stylus:compile',
			'connect:test',
			'watch'
		]);
	});

  grunt.registerTask('build', ['stylus:compile', 'jshint', 'clean:build', 'dojo:dist', 'copy', 'clean:uncompressed',
'connect:dist']);
  grunt.registerTask('default', ['stylus:compile', 'jshint', 'connect:dev', 'watch']);
  grunt.registerTask('test', ['stylus:compile', 'jshint', 'connect:test', 'watch']);
};
