
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
     driver.manage().timeouts().setScriptTimeout(60*1000);
     driver.manage().window().setSize(1920, 1280);

 });

 afterEach(function () {
    driver.quit();
 });


describe('basic test', function () {
	it('should be on correct page', function (done) {

        driver.get('http://edx.akre.biz:8000/');

        driver.getTitle().then(function(title) {
            expect(title).toBe('XBlock scenarios');
            done();
        });

        driver.takeScreenshot().then(function (png) {
            var stream = fs.createWriteStream('/var/lib/jenkins/jobs/Multichoice/workspace/xblock_development/multichoice/tests/images/01-xblock-menu.png');
            stream.write(new Buffer(png, 'base64'));
            stream.end();

        });

        driver.get('http://edx.akre.biz:8000/scenario/multichoice.0/student_view');

        driver.getTitle().then(function(title) {
            expect(title).toBe('XBlock: MultiChoiceXBlock');
            done();
        });

        driver.takeScreenshot().then(function (png) {
            var stream = fs.createWriteStream('/var/lib/jenkins/jobs/Multichoice/workspace/xblock_development/multichoice/tests/images/02-student-view.png');
            stream.write(new Buffer(png, 'base64'));
            stream.end();
        });



/*
        driver.get('http://edx.akre.biz:8000/scenario/multichoice.0/student_view');
        driver.takeScreenshot().then(function (png) {
            var stream = fs.createWriteStream('/var/lib/jenkins/jobs/Multichoice/workspace/xblock_development/multichoice/tests/images/02-student-view.png');
            stream.write(new Buffer(png, 'base64'));
            stream.end();

        });
*/

        /*
                var start = new Date().getTime();
                driver.executeAsyncScript(
                        'window.setTimeout(arguments[arguments.length - 1], 500);').
                    then(function() {
                        console.log(
                            'Elapsed time: ' + (new Date().getTime() - start) + ' ms');
                    });
        */



	}, 10000);
});

