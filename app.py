import requests
import streamlit as st
import random

# Remplace ceci par ton vrai token depuis developer.twitter.com
BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"

keywords = {
    'cope': ['i’m done', 'not selling', 'long term'],
    'rage': ['rugged', 'scam', 'wtf', 'rekt'],
    'hopium': ['buy the dip', 'next bull run', 'we goin up', 'hold'],
    'rug': ['exit', 'rug', 'dump'],
    'bullish': ['gm', 'moon', 'bullish', 'pump'],
    'rekt': ['lost everything', 'zero', 'rekt'],
}

mental_tags = ['borderline', 'schizo bullish', 'maxi', 'exit scammer', 'in denial', 'toxic realist']

def create_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    r = requests.get(url, headers=create_headers())
    if r.status_code != 200:
        raise Exception(f"Erreur : {r.json().get('title', r.text)}")
    return r.json()['data']['id']

def get_user_tweets(user_id, max_results=50):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {"max_results": min(max_results, 100), "tweet.fields": "text"}
    r = requests.get(url, headers=create_headers(), params=params)
    if r.status_code != 200:
        raise Exception(f"Erreur : {r.json().get('title', r.text)}")
    return [tweet["text"] for tweet in r.json().get("data", [])]

def analyze_tweets(tweets):
    summary = {k: 0 for k in keywords}
    for tweet in tweets:
        text = tweet.lower()
        for key, terms in keywords.items():
            if any(term in text for term in terms):
                summary[key] += 1
    return summary

def generate_diagnostic(handle, summary):
    total = sum(summary.values())
    if total == 0:
        return f"@{handle} semble anormalement stable. Probablement un bot, un moine zen ou un sociopathe fonctionnel."

    dominant = max(summary, key=summary.get)
    diagnosis = {
        'cope': "Vit dans le passé, refuse d'accepter les pertes. Risque élevé de schizophrénie bullish.",
        'rage': "Profil explosif. Probablement déjà en guerre avec au moins 3 devs de shitcoins.",
        'hopium': "Déconnecté de la réalité. Consomme de l'espoir pur à haute dose.",
        'rug': "Soit il se fait rug, soit il rug lui-même. À surveiller de très près.",
        'bullish': "Trop optimiste pour son propre bien. Peut se réveiller un matin à -95%.",
        'rekt': "Est passé par la guerre. Comportement apathique ou cynique.",
    }
    personality = random.choice(mental_tags)

    return f"""
🧠 **Analyse de @{handle}**

**Comportement dominant :** `{dominant.upper()}`
**Personnalité crypto :** `{personality}`

**Résumé :**
{diagnosis[dominant]}

---

📊 **Détails bruts :** `{summary}`
"""

st.set_page_config(page_title="Mental Health X-ray 🔍🧠", layout="centered")
st.title("🧠 Crypto Mental Health Scanner")
st.caption("Un outil inutile mais indispensable pour diagnostiquer tes frérots sur Crypto Twitter.")

handle = st.text_input("Entre le @handle Twitter à analyser (sans le @)")

if st.button("Lancer l’analyse mentale") and handle:
    try:
        user_id = get_user_id(handle)
        tweets = get_user_tweets(user_id)
        if not tweets:
            st.warning("Aucun tweet disponible pour ce compte.")
        else:
            summary = analyze_tweets(tweets)
            result = generate_diagnostic(handle, summary)
            st.markdown(result)
    except Exception as e:
        st.error(f"Erreur : {e}")
