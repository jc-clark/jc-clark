import requests  # Import the requests library to make HTTP requests
import feedparser  # Import the feedparser library to parse RSS feeds
from string import Template  # Import the Template class from the string module for template substitution
import sys  # Import sys to exit the script if needed

# URL of the freeCodeCamp RSS feed
rss_url = "https://www.freecodecamp.org/news/rss/"

# List of tags to filter by
target_tags = [
    "beginners guide", "beginners", "learning", "python", 
    "javascript", "html", "css", "self-improvement", "git"
]

# Fetch the RSS feed
response = requests.get(rss_url)
feed = feedparser.parse(response.content)

# Filter posts by tags
filtered_posts = []
for post in feed.entries:
    # Check if the post has any of the target tags
    if 'tags' in post:
        # Extract the tag content from CDATA format
        post_tags = [tag.get('term', '').lower().strip() for tag in post.tags]
        
        # Check if any of our target tags match the post tags
        if any(target_tag.lower() in post_tag for target_tag in target_tags for post_tag in post_tags):
            filtered_posts.append(post)
    
    # Stop once we have 2 matching posts
    if len(filtered_posts) >= 2:
        break

# If we don't have exactly 2 filtered posts, exit without updating
if len(filtered_posts) != 2:
    print(f"Not enough filtered posts found. Only found {len(filtered_posts)} posts matching the tags.")
    print("README not updated.")
    sys.exit(0)  # Exit the script without error

# Extract the two filtered posts with author information
latest_posts = filtered_posts[:2]
news_posts = []
for post in latest_posts:
    author = post.get('author', '')
    if not author and hasattr(post, 'creator'):
        author = post.creator
    news_posts.append(f"<a href='{post.link}'>{post.title}</a> by {author}")

# Debug prints to verify extracted data
for i, post in enumerate(news_posts, 1):
    print(f"news_post_{i}: {post}")
    
    # Also print tags to help debug
    if i <= len(filtered_posts):
        if 'tags' in filtered_posts[i-1]:
            tags = [tag.get('term', '') for tag in filtered_posts[i-1].tags]
            print(f"  Tags: {', '.join(tags)}")

# Read the template file
with open("README.md.tpl", "r") as tpl_file:
    tpl_content = tpl_file.read()

# Replace placeholders with actual posts
template = Template(tpl_content)
readme_content = template.substitute(
    news_post_1=news_posts[0],
    news_post_2=news_posts[1]
)

# Debug print to verify the final content
print("Updated README content:")
print(readme_content)

# Write the updated content to README.md
with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)

print("README successfully updated with 2 filtered posts!")
