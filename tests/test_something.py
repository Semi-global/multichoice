"""Tests for the thumbs module"""

from workbench import scenarios
from workbench.test.selenium_test import SeleniumTest

from pyvirtualdisplay import Display
from selenium import webdriver


class ThreeThumbsTest(SeleniumTest):
    """Test the functionalities of the three thumbs test XBlock."""

    def setUp(self):

        display = Display(visible=0, size=(1024, 768))
        display.start()
        browser = webdriver.Firefox()
        self.browser = browser

        super(ThreeThumbsTest, self).setUp()

        '''
        scenarios.add_xml_scenario(
            "test_three_thumbs", "three thumbs test",
            """<vertical_demo><multichoice/></vertical_demo>"""
        )
        '''

        '''
        self.addCleanup(scenarios.remove_scenario, "test_three_thumbs")
        '''

        # Suzy opens the browser to visit the workbench
        self.browser.get(self.live_server_url)

        # She knows it's the site by the header
        header1 = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(header1.text, 'XBlock scenarios')

    def test_three_thumbs_initial_state(self):
        link = self.browser.find_element_by_link_text('MultiChoiceXBlock')
        link.click()

        header1 = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(header1.text, 'XBlock: MultiChoiceXBlock')

        cnt = self.browser.find_element_by_css_selector('#count_val')
        self.assertEqual(cnt.text, '0')

        cntControl = self.browser.find_element_by_css_selector('#count_btn')
        cntControl.click()

        cnt = self.browser.find_element_by_css_selector('#count_val')
        self.assertEqual(cnt.text, '1')


