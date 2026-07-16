import streamlit as st
import time
from src.generate import generate_recommendations
from src.retriever import retrieve

def recommend(query):
    with st.spinner("Searching similar problems..."):
        context = retrieve(query)
        recommendations = generate_recommendations(query, context)

    st.success("Recommendations generated!")
    st.subheader("Recommendations")
    st.markdown(recommendations.content)

    with st.expander("Retrieved Context"):
        if context["metadatas"]:
            st.json(context["metadatas"][0])
        else:
            st.info("No context retrieved.")

st.set_page_config(
    page_title="OJ Problem Recommender",
    page_icon="💻",
    layout="wide"
)

st.title("💻 OJ Problem Recommender")

query = st.text_input("Enter your problem")

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a problem.")
        st.stop()

    try:
        recommend(query)

    except Exception as e:
        st.error(str(e))