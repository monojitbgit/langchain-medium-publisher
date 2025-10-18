# 🧠 LangChain Medium Auto Publisher

Automate the process of generating and publishing blog posts to **Medium** using **LangChain**, **OpenAI**, and the **Medium API** — all based on topics scheduled in a simple CSV file.

---

## 🚀 Features

- 🗓 **Automated Posting** — Publishes the blog scheduled for the current date.
- 🧩 **LangChain Integration** — Uses `ChatOpenAI` to generate human-like, high-quality content.
- 🖼 **Image Upload Support** — Optionally uploads an image to Medium and embeds it in the post.
- 📘 **Customizable Prompt** — Fine-tune how AI writes your company blogs.
- 🧾 **Logging** — Tracks each execution in a log file (`log.txt`).

---

## 📁 Project Structure

<br>|
<br>├── main.py # Main automation script
<br>├── blog.csv # CSV file containing topics and product links
<br>├── 1log.txt # Log file with execution history
<br>├── README.md # Documentation
<br>└── requirements.txt

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites

<br>- Python **3.9+**
<br>- A valid **OpenAI API Key**
<br>- A **Medium Integration Token**  
  → Generate from your Medium account settings:  
  [https://medium.com/me/settings](https://medium.com/me/settings)

---

### 2️⃣ Installation

Clone the repository:
```bash
git clone https://github.com/monojitbgit/langchain-medium-publisher.git
```

Nevigate to the diractory
```bash
cd langchain-medium-publisher-main
```

Install required dependencies:
```bash
pip install -r requirements.txt
```

or run
```bash
pip install langchain-openai langchain-core requests opencv-python
```

---
### 3️⃣ Configuration

Open medium_post.py and replace placeholders with your credentials:
<br>os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
<br>MEDIUM_API_TOKEN = "your_medium_integration_token_here"

---

### 5️⃣ Run the Script

Execute the Python script:

```bash
python main.py
```

## 🧰 Technologies Used

<br>LangChain
<br>OpenAI GPT Models
<br>Medium API
<br>Python Libraries: requests, csv, datetime, opencv-python

<p align="left"> <a href="https://python.langchain.com/"> <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white" alt="LangChain"/> </a> <a href="https://platform.openai.com/docs/models"> <img src="https://img.shields.io/badge/OpenAI%20GPT%20Models-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI GPT Models"/> </a> <a href="https://github.com/Medium/medium-api-docs"> <img src="https://img.shields.io/badge/Medium%20API-00AB6C?style=for-the-badge&logo=medium&logoColor=white" alt="Medium API"/> </a> </p>

---

## 🧾 License

This project is licensed under the MIT License.
<br>You’re free to use, modify, and distribute it with attribution.
