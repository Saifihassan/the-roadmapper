# 🚀 The RoadMapper

The RoadMapper is an AI-powered application that generates structured learning roadmaps for virtually any topic. It researches the web, curates high-quality learning resources, organizes concepts into progressive learning stages, and delivers a complete roadmap that can be exported in multiple formats.

Whether you're learning web development, video editing, cybersecurity, digital marketing, or any other skill, The RoadMapper provides a clear path from beginner to advanced.

---

## Features

- AI-generated learning roadmaps
- Beginner, Intermediate, and Advanced learning stages
- Structured concepts ordered by difficulty
- Estimated learning duration for each stage
- Curated learning resources including:
  - Documentation
  - Video tutorials
  - Courses
  - Articles
  - Books
- Automatic roadmap review and refinement
- Markdown export
- PDF export
- Notion-compatible export
- Modern Streamlit interface

---

## How It Works

1. Enter any learning topic.
2. The research agent gathers relevant information and learning resources.
3. The roadmap generation agent creates a structured learning path.
4. A review agent validates and improves the roadmap.
5. The final roadmap is displayed and can be exported in multiple formats.

---

## Tech Stack

### Frontend

- Streamlit

### AI Framework

- CrewAI

### Language Models

- OpenRouter
- Gemini
- Groq
- SambaNova
- BluesMinds
- GeneralCompute
- Nara Router

### Search

- Serper API
- Tavily API

### Backend

- Python
- Pydantic

### Export

- Markdown
- PDF (ReportLab)
- Notion-compatible Markdown

---

## Project Structure

```
src/
└── the_roadmapper/
    ├── app.py
    ├── flow.py
    ├── crew.py
    ├── models.py
    ├── config/
    ├── utils/
    └── sample_roadmaps.py
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/the-roadmapper.git
```

Navigate into the project

```bash
cd the-roadmapper
```

Install dependencies

```bash
uv sync
```

Run the application

```bash
uv run streamlit run src/the_roadmapper/app.py
```

---

## Environment Variables

Create a `.env` file containing the required API keys.

```env
SAMBANOVA_API_KEY=
GROQ_API_KEY=
TAVILY_API_KEY=
SERPER_API_KEY=
OPENROUTER_API_KEY=
GEMINI_API_KEY=
NARAROUTER_API_KEY=
OPENAI_BASE_URL=
BLUESMIND_API_KEY=
BLUESMIND_BASE_URL=
GENERALCOMPUTE_API_KEY=
GENERALCOMPUTE_BASE_URL=
```

---

## Example Use Cases

- Frontend Development
- Backend Development
- Full Stack Development
- Mobile App Development
- Machine Learning
- AI Engineering
- Cybersecurity
- UI/UX Design
- Video Editing
- Digital Marketing
- Cold Email Outreach
- DevOps
- Data Science

---

## Roadmap Structure

Each generated roadmap contains:

- Stage description
- Estimated learning duration
- Ordered learning concepts
- Difficulty level
- Priority level
- Curated learning resources
- Resource type classification

---

## License

This project is licensed under the MIT License.