from unittest import TestSuite, makeSuite
from unit_tests.GoogleSearch import GoogleSearch
from HtmlTestRunner import HTMLTestRunner

suite = TestSuite()
suite.addTest(makeSuite(GoogleSearch))
runner = HTMLTestRunner(output='reportes', open_in_browser=True)
runner.run(suite)
