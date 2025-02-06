import requests
import feedparser
from string import Template

# Fetch the RSS feed
rss_url = "https://github.blog/changelog/feed/"
response = requests.get(rss_url)
feed = feedparser.parse(response.content)

# Extract the latest three posts
latest_posts = feed.entries[:3]
changelog_posts = [
    f"<a href='{post.link}'>{post.title}</a>" for post in latest_posts
]

# Read the template file
with open("README.md.tpl", "r") as tpl_file:
    tpl_content = tpl_file.read()

# Replace placeholders with actual posts
template = Template(tpl_content)
readme_content = template.safe_substitute(
    changelog_post_1=changelog_posts[0],
    changelog_post_2=changelog_posts[1],
    changelog_post_3=changelog_posts[2]
)

# Write the updated content to README.md
with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)
