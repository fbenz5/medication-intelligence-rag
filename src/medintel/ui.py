import requests
import streamlit as st

API_URL = "http://localhost:8000"


st.set_page_config(
    page_title="Medication Intelligence",
    page_icon="💊",
    layout="wide",
)

st.title("💊 Medication Intelligence")
st.caption("Evidence-grounded medication information for healthcare professionals.")

query = st.text_area(
    "Ask a medication question",
    placeholder="What are the cardiac risks associated with antiemetic medications?",
    height=100,
)

if st.button("Ask", type="primary", disabled=not query.strip()):
    with st.spinner("Searching evidence and generating answer..."):
        try:
            response = requests.post(
                f"{API_URL}/api/v1/ask",
                json={"query": query},
                timeout=180,
            )
            response.raise_for_status()
            result = response.json()

        except requests.RequestException as exc:
            st.error(f"Unable to contact the API: {exc}")
        else:
            st.subheader("Answer")
            st.write(result["answer"])

            if result["citations"]:
                st.subheader("Sources")

                for citation in result["citations"]:
                    source = citation.get("source") or "Unknown source"
                    title = citation.get("title") or "Unknown document"
                    page = citation.get("page_number")

                    page_text = f", p. {page}" if page is not None else ""

                    st.markdown(
                        f"- **{source}** — {title}{page_text}"
                    )

            if not result["evidence_sufficient"]:
                st.warning(
                    "The available evidence may be insufficient to fully answer this question."
                )