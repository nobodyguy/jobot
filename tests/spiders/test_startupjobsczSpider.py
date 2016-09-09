from scrapy.http import HtmlResponse
from betamax import Betamax
from betamax.fixtures.unittest import BetamaxTestCase
from jobot.spiders.StartupJobsCZ import StartupjobsczSpider


with Betamax.configure() as config:
    # where betamax will store cassettes (http responses):
    config.cassette_library_dir = 'jobot/tests/spiders/responses'
    config.preserve_exact_body_bytes = True


class TestStartupjobsczSpider(BetamaxTestCase):  # superclass provides self.session

    def test_parse(self):
        spider = StartupjobsczSpider()

        # http response is recorded in a betamax cassette:
        response = self.session.get(spider.start_urls[0])

        # forge a scrapy response to test
        scrapy_response = HtmlResponse(body=response.content, url=spider.start_urls[0])

        items = list(spider.parse(scrapy_response))
        del items[len(items)-1]
        self.assertGreater(len(items), 0)

        for item in items:
            with self.subTest(item=item):
                self.assertTrue("www.startupjobs.cz" in item['link'])
                self.assertGreater(len(item['company']), 0)
                self.assertGreater(len(item['location']), 0)
                self.assertGreater(len(item['title']), 0)

