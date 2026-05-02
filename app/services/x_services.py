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

