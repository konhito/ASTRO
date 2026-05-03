run:
	uv run python -m app.main

scrape:
	uv run python -m app.main

install:
	uv pip install -r requirements.txt

setup:
	uv pip install playwright
	uv run playwright install


#it like npm run command thing
# we do make command	
