var By = require('selenium-webdriver').By,
    until = require('selenium-webdriver').until;
    //firefox = require('selenium-webdriver/firefox');
var webdriver = require('selenium-webdriver');


module.exports = function(config) {
    config.set({
        frameworks: ['jasmine'],
        files: [
//            'spec/**/*.js',
  //          '../jstest/*.js'
              '../multichoice/static/js/**/*.js'
        ],
        singleRun: true,
        // define browsers
        reporters: ['progress', 'coverage', 'junit'],
        preprocessors: { '../multichoice/static/js/src/**/*.js': ['coverage'] },
        coverageReporter: {
            dir: 'reports',
            reporters: [
                // reporters not supporting the `file` property
                { type: 'lcov', subdir: 'report-lcov' },
            ]
        },
        junitReporter: {
            outputDir: 'reports/junit',
            outputFile: 'TESTS-xunit.xml', // if included, results will be saved as $outputDir/$browserName/$outputFile
            suite: '', // suite will become the package name attribute in xml testsuite element
            useBrowserName: false // add browser name to report and classes names
        },

        customLaunchers: {
            chrome: {
                base: 'SeleniumWebdriver',
                browserName: 'Chrome',
                getDriver: function(){
                    var driver = new webdriver.Builder()
                        .forBrowser('chrome')
                        .usingServer('http://dev.akre.biz:4444/wd/hub')
                        .build();
                    return driver;
                }
            }
        },
        //browsers: ['swd_firefox']
        browsers: ['chrome']
    });
};
