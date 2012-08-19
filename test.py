from unittest import TestCase
from urlparse import urlparse
import funcs

class TestApp(TestCase):
    def setUp(self):
        self.test_ip = "222.21.32.11"
        self.test_url = "http://testcase.com"

    def tearDown(self):
        r = funcs.redis_client()
        r.hdel("domains", urlparse(self.test_url).hostname)

        safe_ip = funcs.truncate_ip(self.test_ip)
        m = funcs.mc_client()
        m.delete("%s" % safe_ip)


    def testInsertSafe(self):
        for _ in xrange(5):
            funcs.insert_url(self.test_ip, self.test_url)

        for _ in xrange(5):
            count = funcs.insert_url(self.test_ip, "http://www.testcase.com")

        self.assertEqual(10, count)


    def testSpamStop(self):
        for _ in xrange(29):
            funcs.insert_url(self.test_ip, self.test_url)

        with self.assertRaises(funcs.SpamProtectionStop):
            funcs.insert_url(self.test_ip, self.test_url)


    def testMalformedUrl(self):
        r = funcs.insert_url(self.test_ip, "not a url")
        self.assertEqual(r, None)



