import os
import json
import datetime
import csv
import nltk
import ssl
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Setup
ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('punkt')
nltk.data.path.append(os.path.abspath("nltk_data"))

# Load intents
file_path = os.path.abspath("intents.json")
with open(file_path, "r") as file:
    intents = json.load(file)

# Prepare training data
tags, patterns = [], []
for intent in intents:
    for pattern in intent["patterns"]:
        tags.append(intent["tag"])
        patterns.append(pattern)

# Train model
vectorizer = TfidfVectorizer(ngram_range=(1, 4))
x = vectorizer.fit_transform(patterns)
clf = LogisticRegression(random_state=0, max_iter=10000)
clf.fit(x, tags)

# Response generation
def chatbot(input_text):
    input_vector = vectorizer.transform([input_text])
    predicted_tag = clf.predict(input_vector)[0]
    
    for intent in intents:
        if intent["tag"] == predicted_tag:
            return random.choice(intent["responses"])
    return "I'm not sure how to help with that. Could you please rephrase?"

# Custom CSS for styling
import base64

def add_custom_css():
    with open("bg.webp", "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode()

    background_style = f"""
    <style>
    html, body, .stApp {{
        height: 100%;
        margin: 0;
        padding: 0;
        background-image: url("data:image/webp;base64,{encoded_img}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center center;
    }}

    /* DARK overlay using ::before */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.7);  /* This is the dark overlay */
        z-index: -1;
    }}

    .main {{
        background-color: rgba(0, 0, 0, 0.65);
        padding: 2rem;
        border-radius: 16px;
        color: white;
    }}

    .stTextInput > div > div > input {{
        border-radius: 12px;
        padding: 12px;
        font-size: 16px;
        background-color: #1c1c1c;
        color: white;
        border: 1px solid #00aaff;
    }}

    .stTextArea textarea {{
        border-radius: 12px;
        padding: 14px;
        font-size: 16px;
        background: rgba(255, 255, 255, 0.1);
        color: white;
        font-weight: 500;
    }}

    h1, h2, h3 {{
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }}

    .chatbox {{
        background-color: rgba(0, 0, 0, 0.5);
        padding: 20px;
        border-radius: 16px;
        color: white;
    }}

    .block-container {{
        margin-top: -20px;
        max-width: 900px;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)



# Chat counter for Streamlit session
counter = 0

def main():
    global counter
    st.set_page_config(page_title="TourMate Chatbot", page_icon="🧳", layout="wide")
    add_custom_css()

    st.title("🧭 TourMate – Your AI Travel Companion")
    st.markdown("### Discover destinations, find hotels, and plan your perfect trip! 🌍")

    menu = ["💬 Home", "🗂️ Conversation History", "ℹ️ About"]
    choice = st.sidebar.selectbox("Choose an option", menu)

    if choice == "💬 Home":
        st.subheader("Start your travel chat!")

        if not os.path.exists("chat_log.csv"):
            with open("chat_log.csv", "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["User Input", "Chatbot Response", "Timestamp"])

        counter += 1

        with st.container():
            st.markdown('<div class="chatbox">', unsafe_allow_html=True)

            user_input = st.text_input("✈️ You:", key=f"user_input_{counter}")

            if user_input:
                response = chatbot(user_input)
                st.text_area("🤖 TourMate:", value=response, height=150, key=f"response_{counter}")

                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("chat_log.csv", "a", newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([user_input, response, timestamp])

                if response.lower() in ["goodbye", "bye"]:
                    st.success("Thanks for chatting! Safe travels! 🌴")
                    st.stop()

            st.markdown('</div>', unsafe_allow_html=True)

    elif choice == "🗂️ Conversation History":
        st.header("📝 Your Past Conversations")
        if os.path.exists("chat_log.csv"):
            with open("chat_log.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    st.markdown(f"**🧍 You:** {row[0]}")
                    st.markdown(f"**🤖 TourMate:** {row[1]}")
                    st.caption(f"🕒 {row[2]}")
                    st.markdown("---")
        else:
            st.warning("No conversation history found yet.")

    elif choice == "ℹ️ About":
        st.header("📌 About TourMate")
        st.write("""
        **TourMate** is your personalized travel assistant chatbot powered by Machine Learning.

        **🔧 Built with:**
        - Logistic Regression for intent detection
        - NLP (TF-IDF + NLTK) for understanding user queries
        - Streamlit for the beautiful interface

        **🌟 You can ask about:**
        - Tourist attractions, nature, monuments, festivals, wellness spots
        - Hotel suggestions in your chosen destination

        **🚀 Future Enhancements:**
        - Map and location integration
        - Speech-to-text support
        - Personalized plans based on budget & preferences
        """)

if __name__ == "__main__":
    main()
