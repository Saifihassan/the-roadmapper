import streamlit as st
from the_roadmapper.flow import RoadmapFlow
import json
from utils.export_utils import roadmap_to_markdown,roadmap_to_pdf

def strip_code_fences(text: str) -> str:
    cleaned = text.strip()

    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned[3:-3].strip()

        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

    return cleaned


def set_topic():
    st.session_state.topic = st.session_state.suggestion

DEV_MODE=False

BACKEND_ROADMAP={
    "beginner": {
        "description": "Master the foundational concepts of backend development including programming fundamentals, basic databases, HTTP protocol, and simple API creation.",
        "estimated_weeks": 12,
        "concepts": [
            {
                "name": "Programming Fundamentals with a Backend Language",
                "resources": [
                    {
                        "title": "Python for Everybody",
                        "url": "https://www.coursera.org/specializations/python",
                        "type": "course"
                    },
                    {
                        "title": "JavaScript.info",
                        "url": "https://javascript.info/",
                        "type": "documentation"
                    },
                    {
                        "title": "Go by Example",
                        "url": "https://gobyexample.com/",
                        "type": "article"
                    }
                ],
                "completed": False,
                "difficulty": "Easy",
                "priority": "Must-do"
            },
            {
                "name": "Version Control with Git",
                "resources": [
                    {
                        "title": "Git Handbook",
                        "url": "https://guides.github.com/introduction/git-handbook/",
                        "type": "article"
                    },
                    {
                        "title": "Git & GitHub for Beginners",
                        "url": "https://www.youtube.com/watch?v=RGOj5yH7evk",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Easy",
                "priority": "Must-do"
            },
            {
                "name": "Understanding HTTP and REST APIs",
                "resources": [
                    {
                        "title": "HTTP Basics",
                        "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview",
                        "type": "documentation"
                    },
                    {
                        "title": "REST API Tutorial",
                        "url": "https://restfulapi.net/",
                        "type": "article"
                    },
                    {
                        "title": "What is REST?",
                        "url": "https://www.youtube.com/watch?v=CFn9O1Cq3cU",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Easy",
                "priority": "Must-do"
            },
            {
                "name": "Relational Database Fundamentals",
                "resources": [
                    {
                        "title": "SQL Tutorial",
                        "url": "https://www.w3schools.com/sql/",
                        "type": "course"
                    },
                    {
                        "title": "PostgreSQL Documentation",
                        "url": "https://www.postgresql.org/docs/",
                        "type": "documentation"
                    },
                    {
                        "title": "Database Design for Developers",
                        "url": "https://www.youtube.com/watch?v=1Y1TegZXE_s",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Medium",
                "priority": "Must-do"
            },
            {
                "name": "Building Basic REST APIs",
                "resources": [
                    {
                        "title": "REST API with Express",
                        "url": "https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs",
                        "type": "documentation"
                    },
                    {
                        "title": "Flask Mega-Tutorial",
                        "url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world",
                        "type": "course"
                    }
                ],
                "completed": False,
                "difficulty": "Medium",
                "priority": "Must-do"
            },
            {
                "name": "Command Line Basics",
                "resources": [
                    {
                        "title": "Command Line Crash Course",
                        "url": "https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line",
                        "type": "article"
                    },
                    {
                        "title": "Linux Command Line Basics",
                        "url": "https://www.udacity.com/course/shell-workshop--ud206",
                        "type": "course"
                    }
                ],
                "completed": False,
                "difficulty": "Easy",
                "priority": "Must-do"
            }
        ]
    },
    "intermediate": {
        "description": "Build on fundamentals with authentication, ORMs, caching strategies, testing, and deployment practices.",
        "estimated_weeks": 16,
        "concepts": [
            {
                "name": "Database ORM and Query Builders",
                "resources": [
                    {
                        "title": "SQLAlchemy Tutorial",
                        "url": "https://docs.sqlalchemy.org/en/20/tutorial/",
                        "type": "documentation"
                    },
                    {
                        "title": "Prisma ORM Guide",
                        "url": "https://www.prisma.io/docs/guides",
                        "type": "documentation"
                    },
                    {
                        "title": "TypeORM Tutorial",
                        "url": "https://typeorm.io/",
                        "type": "documentation"
                    }
                ],
                "completed": False,
                "difficulty": "Medium",
                "priority": "Must-do"
            },
            {
                "name": "Authentication and Authorization",
                "resources": [
                    {
                        "title": "OAuth 2.0 Overview",
                        "url": "https://oauth.net/2/",
                        "type": "documentation"
                    },
                    {
                        "title": "JWT Introduction",
                        "url": "https://jwt.io/introduction/",
                        "type": "article"
                    },
                    {
                        "title": "Authentication Systems Explained",
                        "url": "https://www.youtube.com/watch?v=sbVevkJvaRs",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Medium",
                "priority": "Must-do"
            },
            {
                "name": "API Security Best Practices",
                "resources": [
                    {
                        "title": "OWASP API Security Top 10",
                        "url": "https://owasp.org/API-Security/",
                        "type": "documentation"
                    },
                    {
                        "title": "API Security Guide",
                        "url": "https://www.youtube.com/watch?v=aUfPf-cl0q4",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Medium",
                "priority": "Must-do"
            },
            {
                "name": "Caching Strategies",
                "resources": [
                    {
                        "title": "Caching Guide",
                        "url": "https://redis.io/docs/manual/patterns/",
                        "type": "documentation"
                    },
                    {
                        "title": "Redis University",
                        "url": "https://university.redis.com/",
                        "type": "course"
                    },
                    {
                        "title": "HTTP Caching",
                        "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching",
                        "type": "documentation"
                    }
                ],
                "completed": False,
                "difficulty": "Medium",
                "priority": "Must-do"
            },
            {
                "name": "Testing Backend Applications",
                "resources": [
                    {
                        "title": "Testing JavaScript",
                        "url": "https://testingjavascript.com/",
                        "type": "course"
                    },
                    {
                        "title": "PyTest Guide",
                        "url": "https://docs.pytest.org/en/7.4.x/",
                        "type": "documentation"
                    },
                    {
                        "title": "Integration Testing for APIs",
                        "url": "https://www.youtube.com/watch?v=6dV5fwq3VYw",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Medium",
                "priority": "Must-do"
            },
            {
                "name": "Containerization with Docker",
                "resources": [
                    {
                        "title": "Docker Official Tutorial",
                        "url": "https://docs.docker.com/get-started/",
                        "type": "documentation"
                    },
                    {
                        "title": "Docker for Beginners",
                        "url": "https://www.youtube.com/watch?v=pTFZFdj4Zuo",
                        "type": "video"
                    },
                    {
                        "title": "Docker Deep Dive",
                        "url": "https://www.amazon.com/Docker-Deep-Dive-Nigel-Poulton/dp/1521822808",
                        "type": "book"
                    }
                ],
                "completed": False,
                "difficulty": "Medium",
                "priority": "Must-do"
            },
            {
                "name": "Deployment and CI/CD Basics",
                "resources": [
                    {
                        "title": "GitHub Actions Tutorial",
                        "url": "https://docs.github.com/en/actions",
                        "type": "documentation"
                    },
                    {
                        "title": "CI/CD Pipeline Explained",
                        "url": "https://www.youtube.com/watch?v=NuNDsNeV3E4",
                        "type": "video"
                    },
                    {
                        "title": "Deploy Your First Container",
                        "url": "https://www.youtube.com/watch?v=2X3UiY4P6aU",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Medium",
                "priority": "Must-do"
            }
        ]
    },
    "advanced": {
        "description": "Master system design, microservices architecture, performance optimization, and scalability patterns for enterprise applications.",
        "estimated_weeks": 20,
        "concepts": [
            {
                "name": "System Design Fundamentals",
                "resources": [
                    {
                        "title": "System Design Primer",
                        "url": "https://github.com/donnemartin/system-design-primer",
                        "type": "article"
                    },
                    {
                        "title": "Designing Data-Intensive Applications",
                        "url": "https://dataintensive.net/",
                        "type": "book"
                    },
                    {
                        "title": "System Design Interview Course",
                        "url": "https://www.educative.io/courses/grokking-the-system-design-interview",
                        "type": "course"
                    }
                ],
                "completed": False,
                "difficulty": "Hard",
                "priority": "Must-do"
            },
            {
                "name": "Microservices Architecture",
                "resources": [
                    {
                        "title": "Microservices Guide",
                        "url": "https://martinfowler.com/microservices/",
                        "type": "article"
                    },
                    {
                        "title": "Building Microservices",
                        "url": "https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/",
                        "type": "book"
                    },
                    {
                        "title": "Microservices Architecture Explained",
                        "url": "https://www.youtube.com/watch?v=jVLXi4RX3aY",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Hard",
                "priority": "Must-do"
            },
            {
                "name": "Message Queues and Event-Driven Architecture",
                "resources": [
                    {
                        "title": "RabbitMQ Tutorial",
                        "url": "https://www.rabbitmq.com/tutorials",
                        "type": "documentation"
                    },
                    {
                        "title": "Apache Kafka Documentation",
                        "url": "https://kafka.apache.org/documentation/",
                        "type": "documentation"
                    },
                    {
                        "title": "Event-Driven Architecture",
                        "url": "https://www.youtube.com/watch?v=rQtBK8qVPhU",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Hard",
                "priority": "Must-do"
            },
            {
                "name": "Performance Optimization and Monitoring",
                "resources": [
                    {
                        "title": "APM Tools Guide",
                        "url": "https://www.datadoghq.com/learning/",
                        "type": "article"
                    },
                    {
                        "title": "Monitoring and Observability",
                        "url": "https://www.youtube.com/watch?v=s0mFAiipXfg",
                        "type": "video"
                    },
                    {
                        "title": "Application Performance Monitoring",
                        "url": "https://www.coursera.org/learn/apm",
                        "type": "course"
                    }
                ],
                "completed": False,
                "difficulty": "Hard",
                "priority": "Must-do"
            },
            {
                "name": "API Gateway and Load Balancing",
                "resources": [
                    {
                        "title": "NGINX Documentation",
                        "url": "https://nginx.org/en/docs/",
                        "type": "documentation"
                    },
                    {
                        "title": "Kong API Gateway",
                        "url": "https://docs.konghq.com/",
                        "type": "documentation"
                    },
                    {
                        "title": "API Gateway Explained",
                        "url": "https://www.youtube.com/watch?v=vWQlua5RyM8",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Medium",
                "priority": "Must-do"
            },
            {
                "name": "GraphQL for Backend Development",
                "resources": [
                    {
                        "title": "GraphQL Official Tutorial",
                        "url": "https://graphql.org/learn/",
                        "type": "documentation"
                    },
                    {
                        "title": "Apollo GraphQL Course",
                        "url": "https://www.apollographql.com/tutorials/",
                        "type": "course"
                    }
                ],
                "completed": False,
                "difficulty": "Hard",
                "priority": "Optional"
            },
            {
                "name": "Distributed Systems Patterns",
                "resources": [
                    {
                        "title": "Distributed Systems Patterns",
                        "url": "https://martinfowler.com/articles/patterns-of-distributed-systems/",
                        "type": "article"
                    },
                    {
                        "title": "Site Reliability Engineering",
                        "url": "https://sre.google/sre-book/table-of-contents/",
                        "type": "book"
                    },
                    {
                        "title": "Consensus in Distributed Systems",
                        "url": "https://www.youtube.com/watch?v=IEeVc39hJ9I",
                        "type": "video"
                    }
                ],
                "completed": False,
                "difficulty": "Hard",
                "priority": "Must-do"
            }
        ]
    }
}



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
     

    if DEV_MODE:
        roadmap = BACKEND_ROADMAP
    else:
        flow = RoadmapFlow()
        flow.state.topic = topic

        with st.spinner("Generating roadmap..."):
            flow.kickoff()

        roadmap = json.loads(
            strip_code_fences(flow.state.roadmap_output)
        )
    total_weeks = 0
    total_concepts = 0
    total_resources = 0

    for level in roadmap.values():
        total_weeks += level["estimated_weeks"]
        total_concepts += len(level["concepts"])

        for concept in level["concepts"]:
            total_resources += len(concept["resources"])

    col1,col2 = st.columns([6,1])
    with col1:

        st.title(topic if topic else "Backend Development")
    with col2:
         st.markdown("""
            <style>
            div[data-testid="column"]:last-child{
                padding-top:18\\29px;
            }
            </style>
            """, unsafe_allow_html=True)
         with st.popover("Export to", use_container_width=True):
            markdown_text=roadmap_to_markdown(
                            topic if topic else 'Backend Development',
                            roadmap
                        )
            pdf_bytes = roadmap_to_pdf(
            topic if topic else "Backend Development",
            roadmap,
        )
            st.download_button(
                "📄 Markdown",
                data=markdown_text,
                file_name=f"{topic.lower().replace(' ', '_')}_roadmap.md",
                mime="text/markdown",
                use_container_width=True,
            )

            st.download_button(
                "📑 PDF",
                data=pdf_bytes,
                file_name=f"{topic.lower().replace(' ', '_')}_roadmap.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

            st.download_button(
                "📝 Notion",
                data=markdown_text,
                file_name=f"{topic.lower().replace(' ', '_')}_roadmap.md",
                mime="text/markdown",
                use_container_width=True,
            )
            st.caption("Import this Markdown file directly into Notion.")

    c1, c2, c3 = st.columns(3)

    c1.metric("⏱ Weeks", total_weeks)
    c2.metric("📚 Concepts", total_concepts)
    c3.metric("🔗 Resources", total_resources)

    st.divider()

  

    icons = {
        "video": "🎥",
        "course": "📚",
        "documentation": "📖",
        "article": "📄",
        "book": "📕",
    }

    level_icons = {
        "beginner": "🟢",
        "intermediate": "🟡",
        "advanced": "🔴",
    }

    for level_name in ["beginner", "intermediate", "advanced"]:

        level = roadmap[level_name]

        with st.expander(
            f"{level_icons[level_name]} {level_name.title()}",
            expanded=(level_name == "beginner"),
        ):

            st.markdown(level["description"])
            st.caption(f"Estimated Duration: {level['estimated_weeks']} weeks")

            st.divider()

            for concept in level["concepts"]:

                st.markdown(f"{concept["name"]}")

                st.divider()

                left, right = st.columns(2)

                with left:
                    st.caption(f"🟢 Difficulty: {concept['difficulty']}")
                    st.write("Resources")

                with right:
                    st.caption(f"⭐ Priority: {concept['priority']}")

                for resource in concept["resources"]:
                    icon = icons.get(resource["type"], "")

                    st.markdown(
                        f"{icon} [{resource['title']}]({resource['url']})"
                    )

                st.divider()

   
   