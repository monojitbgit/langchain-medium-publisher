import os
import csv
import re
from datetime import datetime
import requests
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
import cv2

# ==============================
# CONFIGURATION
# ==============================

# Log execution time
current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
with open("log.txt", "a") as f:
    f.write(f"{current_time}: LangChain Medium posting script run.\n")

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Medium API token
MEDIUM_API_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# ==============================
# FUNCTIONS
# ==============================

def get_medium_user_id():
    """Retrieve the user ID for the Medium account."""
    url = "https://api.medium.com/v1/me"
    headers = {
        "Authorization": f"Bearer {MEDIUM_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['id']
    else:
        print("❌ Failed to retrieve Medium user ID:", response.json())
        return None

MEDIUM_USER_ID = get_medium_user_id()

def read_topics(file_path):
    """Read topics from CSV."""
    topics = []
    with open(file_path, mode='r', encoding='windows-1252') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            topics.append((row['DATE'], row['TOPICS'], row['IMAGES'], row['Product Page Link']))
    return topics

def parse_date(date_str):
    """Parse date in format 'dd-mm-yyyy'."""
    return datetime.strptime(date_str, '%d-%m-%Y')

def upload_image_to_medium(image_file_path):
    """Upload image to Medium and return URL."""
    url = "https://api.medium.com/v1/images"
    headers = {
        "Authorization": f"Bearer {MEDIUM_API_TOKEN}",
        "Accept": "application/json"
    }
    with open(image_file_path, 'rb') as image_file:
        files = {'image': (os.path.basename(image_file_path), image_file, 'image/png')}
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 201:
            return response.json()['data']['url']
        else:
            print("❌ Failed to upload image:", response.json())
            return None

def insert_image_in_content(content, image_url):
    """Insert an image URL at the top of the blog post."""
    if not image_url:
        return content
    return f"![Image]({image_url})\n\n{content}"

def post_to_medium(title, content, hashtags):
    """Post content to Medium."""
    url = f"https://api.medium.com/v1/users/{MEDIUM_USER_ID}/posts"
    headers = {
        "Authorization": f"Bearer {MEDIUM_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "title": title,
        "contentFormat": "markdown",
        "content": content,
        "tags": hashtags,
        "publishStatus": "public"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("✅ Blog posted successfully on Medium!")
    else:
        print("❌ Failed to post on Medium:", response.json())

def extract_hashtags(content):
    """Extract hashtags if specified in content."""
    match = re.search(r'Hashtags: (.+)', content)
    if match:
        hashtags = match.group(1).split(', ')
        return hashtags
    return []

def generate_and_post_blog(date, topic, image_file, product_page_link):
    """Generate and post a blog article to Medium."""
    try:
        prompt_text = (
            "You are a content writer working at Example Private Limited, a supplier of mild steel materials "
            "(not stainless steel or cold rolled). The company operates PAN India and supplies only mild and hot rolled steel.\n\n"
            "Write an informative, engaging, 800–1000 word blog post on the following topic.\n"
            "Mention 'Example Private Limited' 2–3 times in the middle, but focus on the topic content.\n\n"
            f"Topic: {topic}\nDate: {date}\n"
        )

        prompt = ChatPromptTemplate.from_template(prompt_text)
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        chain = RunnableSequence(prompt, model, StrOutputParser())

        blog_content = chain.invoke({})

        hashtags = extract_hashtags(blog_content)
        blog_content = f"# {topic}\n\n{blog_content}\n\nProduct Page: {product_page_link}\n\nWebsite: https://example.com/"

        if image_file and os.path.exists(image_file):
            image_url = upload_image_to_medium(image_file)
            blog_content = insert_image_in_content(blog_content, image_url)

        post_to_medium(topic, blog_content, hashtags)

    except Exception as e:
        print(f"❌ Error generating blog for '{topic}': {str(e)}")

# ==============================
# EXECUTION
# ==============================

topics_file_path = 'blog.csv'
topics = read_topics(topics_file_path)
today = datetime.today()
found_today = False

for date, topic, image_file, product_page_link in topics:
    topic_date = parse_date(date)
    if topic_date.date() == today.date():
        image_path = f'C:\\Users\\User\\Documents\\VSCODE\\Blog\\{image_file}'
        if not image_file.lower().endswith('.png'):
            image_path += '.png'
        generate_and_post_blog(date, topic, image_path, product_page_link)
        found_today = True

if not found_today:
    print("📅 No topics scheduled for today.")

