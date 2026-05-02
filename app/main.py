from app.services.x_services import XService
from app.utils.data_loader import load_data;
from app.utils.data_saver import save_post;
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()



if __name__ == "__main__":
    #created a instance of the class kinda
    x = XService(headless=False)  # keep False for testing

    users = load_data("data/x_user.json")

    all_posts = []

    for i in users:
        username = i["username"]
        #this only works when logged in
        include_replies = i.get("include_replies", False)

        print(f"\n=== {username} (replies={include_replies}) ===")

        posts = x.get_posts(username, 10,include_replies)
        for p in posts:
            all_posts.append({
                "username": username,
                "content": p,
                "timestamp": datetime.now().isoformat(),
                "source": "x"
            })
        save_post(all_posts, "data/posts.json")



#    posts = x.get_posts("elonmusk", 10)

    for i, p in enumerate(posts, 1):
        print(f"{i}. {p}\n")
