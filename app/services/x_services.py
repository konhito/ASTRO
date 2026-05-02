# import requests

# class XScraper:
#   def __init__(self):
#     self.url = "https://x.com/i/api/graphql/Ob0lCmufQqqLTwh_Wck5XA/UserTweets"
#     self.headers = {
#         "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs",
#         "user-agent": "Mozilla/5.0",
#         "x-twitter-active-user": "yes",
#         "x-twitter-client-language": "en"
#     }
#     def get_post(self,uder_id,count=10):
#       param = {
#         "variables": f'{{"userId":"{user_id}","count":{count}}}',
#         "features": "{}"
#       }
#       res = requests.get(self.url,headers=self.headers,params=param)
#       return res.json()

#this approach will mostry fail because of rotating things to tackle this we will use playwrite
from playwright.sync_api import sync_playwright


class XService:
    def __init__(self, headless=True):
        self.headless = headless

    def _start_browser(self):
        self.p = sync_playwright().start()

        self.browser = self.p.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        self.page = self.context.new_page()

    def _close_browser(self):
        self.browser.close()
        self.p.stop()

    def get_posts(self, username, count=10):
        self._start_browser()

        try:
            self.page.goto(f"https://x.com/{username}", timeout=60000)

            # wait for tweets to load
            self.page.wait_for_selector("article", timeout=60000)

            # scroll a bit to load more tweets
            for _ in range(3):
                self.page.mouse.wheel(0, 2000)
                self.page.wait_for_timeout(2000)

            tweets = self.page.locator("article").all_text_contents()

            return tweets[:count]

        except Exception as e:
            print("Error:", e)
            return []

        finally:
            self._close_browser()
