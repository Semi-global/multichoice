
var webdriver = require('selenium-webdriver');
fs = require('fs');
stream = require('stream');
//var driver = new webdriver.Builder().withCapabilities(webdriver.Capabilities.chrome()).build();

    var driver = new webdriver.Builder()
    .forBrowser('chrome')
    .usingServer('http://dev.akre.biz:4444/wd/hub')
    .build();

/*
    this.driver = new selenium.Builder()
    .forBrowser('firefox')
    .usingServer('http://localhost:4444/wd/hub')
    .build();
 */
 beforeEach(function() {
     driver.manage().timeouts().setScriptTimeout(6000);
     driver.manage().window().setSize(400, 800);

 });

 afterEach(function () {
    driver.quit();
 });


describe('basic test', function () {
	it('should be on correct page', function (done) {

        driver.get('http://wingify.com');

        driver.takeScreenshot().then(function (png) {
            var stream = fs.createWriteStream('/var/lib/jenkins/jobs/Multichoice/workspace/xblock_development/multichoice/tests/images/asdf.png');
            stream.write(new Buffer(png, 'base64'));
            stream.end();

        });

        var start = new Date().getTime();
        driver.executeAsyncScript(
                'window.setTimeout(arguments[arguments.length - 1], 500);').
            then(function() {
                console.log(
                    'Elapsed time: ' + (new Date().getTime() - start) + ' ms');
            });

        driver.takeScreenshot().then(function (png) {
            var stream = fs.createWriteStream('/var/lib/jenkins/jobs/Multichoice/workspace/xblock_development/multichoice/tests/images/asdf2.png');
            stream.write(new Buffer(png, 'base64'));
            stream.end();

        });

        driver.getTitle().then(function(title) {
			expect(title).toBe('Wingify');
			// Jasmine waits for the done callback to be called before proceeding to next specification.
			done();
		});

	}, 10000);
});

