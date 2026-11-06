import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Ultimate All-Rounder Agent", page_icon="⚡", layout="centered")

MY_PASSWORD = "8899"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 प्राइवेट AI एजेंट लॉगिन")
    pwd = st.text_input("अपना सीक्रेट पासवर्ड दर्ज करें:", type="password")
    if st.button("लॉगिन करें"):
        if pwd == MY_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("गलत पासवर्ड! कृपया सही पासवर्ड डालें।")
    st.stop()

st.title("⚡ पर्सनल ऑल-राउंडर AI एजेंट")
st.caption("शेयर मार्केट • फैंटेसी स्पोर्ट्स • वायरल कंटेंट • सरकारी योजनाएं • बिजनेस • कैलकुलेशन")

API_KEY = "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"

def search_web(query):
    try:
        with DDGS() as ddgs:
            res = list(ddgs.text(query, max_results=4))
            return "\n".join([f"- {r['title']}: {r['body']}" for r in res])
    except Exception:
        return ""

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

user_query = st.chat_input("हुकुम दें भाई, क्या काम करना है?")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        status = st.empty()
        status.text("जानकारी जुटाई जा रही है...")
        
        web_info = search_web(user_query)
        
        system_instruction = f"""
तुम यूजर के 100% वफादार, सुपर-इंटेलिजेंट ऑल-राउंडर पर्सनल AI एजेंट हो।

तुम्हारी विशेषज्ञता के मुख्य क्षेत्र:
1. शेयर मार्केट, डीमैट व क्रिप्टो: शेयर भाव, ब्रेकआउट लेवल्स, निफ्टी/बैंकनिफ्टी, गोल्ड रेट्स व क्रिप्टोकरेंसी।
2. फैंटेसी स्पोर्ट्स (क्रिकेट/फुटबॉल): पिच रिपोर्ट, मैच-अप्स, टॉस इम्पैक्ट, फैंटेसी पॉइंट्स व बेस्ट Captain / Vice-Captain पिक्स।
3. सोशल मीडिया व कंटेंट क्रिएशन: यूट्यूब शॉर्ट्स/फेसबुक रील्स के लिए वायरल भोजपुरी व हिंदी स्क्रिप्ट्स, कॉमिक पंचलाइन्स, AI वीडियो प्रॉम्प्ट्स व हैशटैग्स।
4. सरकारी योजनाएं व सब्सिडी: केंद्र व राज्य सरकार की योजनाएं, लोन, फॉर्म भरने के नियम व पात्रता।
5. बिजनेस, कमाई व लीगल सलाह: कम बजट के बिजनेस आइडियाज, मार्केटिंग स्ट्रैटेजी और सामान्य कानूनी दस्तावेज व नियम।
6. गणित व हिसाब-किताब: ब्याज, लोन ईएमआई, नफा-नुकसान का तेज व सटीक कैलकुलेशन।

इंटरनेट से ताजा संदर्भ:
{web_info}

निर्देश:
- बिना किसी फालतू ज्ञान या उपदेश के सीधे और सरल भाषा में सटीक उत्तर दो।
- अगर यूजर भोजपुरी या हिंदी में पूछे, तो उसी लहजे में दोस्ताना और व्यावहारिक जवाब दो।
"""

        models_to_try = [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "llama3-8b-8192"
        ]

        client = Groq(api_key=API_KEY)
        success = False
        for model_name in models_to_try:
            try:
                chat_completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_query}
                    ]
                )
                reply = chat_completion.choices[0].message.content
                status.empty()
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                success = True
                break
            except Exception:
                continue
        
        if not success:
            status.empty()
            st.error("AI मॉडल लोड हो रहा है, कृपया 10 सेकंड बाद पुनः प्रश्न पूछें।")
