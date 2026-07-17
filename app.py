import streamlit as st
import time
from src.generate import generate_recommendations
from src.retriever import retrieve

def get_recommendation_label(distance):
    if distance < 0.35:
        return "🟢 Strong Recommendation"
    elif distance < 0.45:
        return "🟡 Good Recommendation"
    else:
        return "🔵 Related Topic"

def recommend(query):
    with st.spinner("Searching similar problems..."):
        context = retrieve(query)
        recommendations = generate_recommendations(query, context)

    st.success("Recommendations generated!")
    st.subheader("Recommendations")
    st.markdown(recommendations.content)

    if context["metadatas"] and context["metadatas"][0]:
        for meta, dist in zip(context["metadatas"][0], context["distances"][0]):

            with st.expander(
                f"{meta['title']} • {get_recommendation_label(dist)}",
                expanded=False,
            ):
                st.write(f"**Pattern:** {meta['pattern']}")
                st.write(f"**Difficulty:** {meta['difficulty']}")
                st.write(f"**Core Idea:** {meta['coreIdea']}")
                st.write(f"**Techniques:** {', '.join(meta['techniques'])}")

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