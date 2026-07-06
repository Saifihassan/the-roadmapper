import streamlit as st
from the_roadmapper.flow import RoadmapFlow
import json


def strip_code_fences(text: str) -> str:
    cleaned = text.strip()

    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned[3:-3].strip()

        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

    return cleaned


def set_topic():
    st.session_state.topic = st.session_state.suggestion



Generation_text = [
    "Getting started",
    "Analyzing the best learning path",
    "Curating resources",
    "Building roadmap",
    "Adding final touches",
]
st.set_page_config(page_title="The Roadmapper", page_icon="📖", layout="wide")



if "selected_topic" not in st.session_state:
        st.session_state.selected_topic = ""
with st.sidebar:
    st.title("The RoadMapper")
    st.caption("Generate structured learning roadmaps powered by AI")
    st.divider()
    topic = st.text_input(
    "Topic",
    value=st.session_state.selected_topic,
    placeholder="e.g Cold Email Outreach..."
)
    generate = st.button("Generate Roadmap", use_container_width=True)
    st.markdown("### 🔥 Popular Topics")
    # st.caption("Popular searches.")
    popular_topics = [
    "Frontend Development",
    "Backend Development",
    "Fullstack Development",
    "App Development",
    "Video Editing",
    ]
    for item in popular_topics:
        if st.button(
            f"🔍 {item}",
            use_container_width=True,
            key=f"topic_{item}"
        ):
            st.session_state.selected_topic = item
            st.rerun()


    

st.subheader("📚 Generated Roadmap")
if not generate:
    st.info(
        "Your personalized roadmap will appear here.\n\n"
        "Choose a topic on the left and click **Generate Roadmap**."
    )
if generate:
    flow = RoadmapFlow()
    flow.state.topic = topic
    with st.spinner("Generating roadmap..."):
        flow.kickoff()
    roadmap = json.loads(strip_code_fences(flow.state.roadmap_output))
    for level in ["beginner", "intermediate", "advanced"]:
        with st.expander(level.title(), expanded=True):
            st.write(roadmap[level]["description"])
            st.write(f"Estimated Weeks: {roadmap[level]['estimated_weeks']}")
            st.divider()
            for concept in roadmap[level]["concepts"]:
                st.subheader(concept["name"])
                st.write(f"Difficulty: {concept['difficulty']}")
                st.write(f"Priority: {concept['priority']}")
                for resource in concept["resources"]:
                    st.markdown(
                        f"- [{resource['title']}]({resource['url']}) "
                        f"({resource['type']})"
                    )
                st.divider()