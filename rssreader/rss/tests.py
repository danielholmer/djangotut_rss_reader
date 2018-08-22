from django.test import TestCase

from django.urls import reverse
from rss.models import Feed
import json



class RssFeedModelTests(TestCase):
    def setUp(self):
        Feed.objects.create(
                url="https://www.svt.se/nyheter/rss.xml"
        )
    def test_model_has_url(self):
        django_feed = Feed.objects.get(
                url="https://www.svt.se/nyheter/rss.xml"
        )

        self.assertEqual(django_feed.url, "https://www.svt.se/nyheter/rss.xml")

class RssRestFeedsViewTests(TestCase):
    """
    Gör egentligen ingenting just nu, men sparar ändå
    """

    def test_create_feed(self):

        url = "https://www.svt.se/nyheter/rss.xml"
        json_data = json.dumps({ "url": url})

        response = self.client.post(
                reverse("rest-feeds"),
                json_data,
                content_type="application/json"
        )
        feeds = Feed.objects.all()

        self.assertEqual(response.status_code, 201)
        self.assertQuerysetEqual(feeds,["<Feed '{}'>".format(url)])

    def test_get_feeds(self):

        url = "https://www.svt.se/nyheter/rss.xml"

        Feed.objects.create(url=url)

        response = self.client.get(reverse('rest-feeds'))
        feed = response.json()[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(feed["url"], url)

    def test_update_feed(self):

        url = "https://www.svt.se/nyheter/rss.xml"
        new_url = "https://utan.io/?feed=rss2"
        Feed.objects.create(url=url)
        json_data = json.dumps({ "url": new_url })

        response = self.client.put(
                "/rss/feeds/1/",
                json_data,
                content_type="application/json"
        )

        feeds = Feed.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(feeds,["<Feed '{}'>".format(new_url)])

    def test_delete_feed(self):
        Feed.objects.create( url="https://www.svt.se/nyheter/rss.xml")

        response = self.client.delete("/rss/feeds/1/")

        feeds = Feed.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(feeds, [] )

class RssRestItemsViewTests(TestCase):

    def test_get_items(self):
        Feed.objects.create(url="https://www.svt.se/nyheter/rss.xml")

        response = self.client.get(reverse("rest-items"))
        self.assertEqual(response.status_code, 200)
