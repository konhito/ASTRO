from app.services.x_services import XService

if __name__ == "__main__":
    x = XService(headless=False)  # keep False for testing

    posts = x.get_posts("elonmusk", 10)

    for i, p in enumerate(posts, 1):
        print(f"{i}. {p}\n")
