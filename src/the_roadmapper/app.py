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


def set_topic_from_button(value: str) -> None:
    st.session_state.topic = value

Generation_text = [
    "Getting started",
    "Analyzing the best learning path",
    "Curating resources",
    "Building roadmap",
    "Adding final touches",
]
st.set_page_config(
    page_title="The Roadmapper",
    page_icon="📖",
    layout="wide"
)

st.title("The RoadMapper")
st.caption("Generate structured learning roadmaps powered by AI")
st.divider()


topic = st.text_input(
    "Topic",
    key="topic",
    placeholder="e.g Cold Email Outreach"
)
col1, col2, col3 = st.columns(3)

with col1:
    st.button(
        "Video Editing",
        use_container_width=True,
        on_click=set_topic_from_button,
        args=("Video Editing",),
    )
    
with col2:
    st.button(
        "App Development",
        use_container_width=True,
        on_click=set_topic_from_button,
        args=("App Development",),
    )

with col3:
    st.button(
        "Fullstack development",
        use_container_width=True,
        on_click=set_topic_from_button,
        args=("Fullstack development",),
    )

col4,col5=st.columns(2)
with col4:
    st.button(
        "Frontend Development",
        use_container_width=True,
        on_click=set_topic_from_button,
        args=("Frontend Development",),
    )
with col5:
    st.button(
        "Backend Development",
        use_container_width=True,
        on_click=set_topic_from_button,
        args=("Backend Development",),
    )
generate = st.button(
    "Generate Roadmap",
    use_container_width=True
)

if generate:
    flow=RoadmapFlow()
    flow.state.topic=topic

    with st.spinner("Generating roadmap..."):
        flow.kickoff()
    roadmap= json.loads(strip_code_fences(flow.state.roadmap_output))


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