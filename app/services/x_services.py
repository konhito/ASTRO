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
#     def get_post(self,user_id,count=10):
#       param = {
#         "variables": f'{{"userId":"{user_id}","count":{count}}}',
#         "features": "{}"
#       }
#       res = requests.get(self.url,headers=self.headers,params=param)
#       return res.json()

#this approach will mostry fail because of rotating things to tackle this we will use playwrite
from playwright.sync_api import sync_playwright
from app.utils.humanize_pause import human_pause

import os


class XService:
    def __init__(self, headless=True):
        self.headless = headless
        self.state_path = "data/state.json"

    def _start_browser(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        # use saved session if exists
        if os.path.exists(self.state_path):
            self.context = self.browser.new_context(storage_state=self.state_path)
        else:
            self.context = self.browser.new_context()

        self.page = self.context.new_page()

    def _close_browser(self):
        self.browser.close()
        self.p.stop()

    def is_logged_in(self):
        self.page.goto("https://x.com/home")
        return not self.page.locator("text=Sign in").is_visible(timeout=5000)

    def login(self):
      username = os.getenv("X_USERNAME")
      password = os.getenv("X_PASSWORD")

      if not username or not password:
          print("Missing credentials")
          return False

      print("Logging in...")
      human_pause(2,4)
      self.page.goto("https://x.com/i/flow/login", timeout=60000)

      print("went to login page")

      # wait for ANY input to appear

      try:
          # STEP 1: username/email
          print("inside try block")
          user_input = self.page.locator('input[autocomplete="username"]').first
          print("user_input found")
          human_pause(2,4)
          
          user_input.click()
          human_pause(2,4)
          print("clicked")
          user_input.type(username, delay=50)
          print("typing")
          human_pause(2,4)
 #         self.page.keyboard.press("Enter")
          next_button = self.page.locator("text=Next")
          human_pause(2,4)
          print("button found")
          next_button.click()

      except:
          print("Username field not found (maybe already logged in?)")
          return True

      self.page.wait_for_timeout(3000)

      # STEP 2: sometimes X asks again for username
      if self.page.locator('input[name="text"]').is_visible():
          self.page.fill('input[name="text"]', username)
          self.page.keyboard.press("Enter")
          self.page.wait_for_timeout(3000)

      # STEP 3: password
      try:
          pass_input = self.page.locator('input[name="password"]').first
          pass_input.wait_for(timeout=15000)
          pass_input.click()
          pass_input.fill(password)
          self.page.keyboard.press("Enter")
      except:
          print("Password step not found")
          return False

      self.page.wait_for_timeout(5000)

      # SAVE SESSION
      self.context.storage_state(path=self.state_path)

      return True

    def get_posts(self, username, count=10, include_replies=False):
        self._start_browser()

        try:
            # ensure login
            if not self.is_logged_in():
                success = self.login()
                if not success:
                    return []

            url = f"https://x.com/{username}"
            if include_replies:
                url += "/with_replies"

            self.page.goto(url, timeout=60000)

            self.page.wait_for_selector("article", timeout=60000)

            # scroll to load more
            for _ in range(3):
                self.page.mouse.wheel(0, 2000)
                self.page.wait_for_timeout(2000)

            tweets = self.page.locator("article div[lang]").all_text_contents()

            return tweets[:count]

        except Exception as e:
            print("Error:", e)
            return []

        finally:
            self._close_browser()
