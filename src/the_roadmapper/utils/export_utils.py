from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

def roadmap_to_markdown(topic:str,roadmap:dict)->str:
    """Convert a roadmap dictionary into Markdown."""

    icons = {
        "video": "🎥",
        "course": "📚",
        "documentation": "📖",
        "article": "📄",
        "book": "📕",
    }

    lines = []

   

    lines.append(f"# {topic}")
    lines.append("")

    if roadmap["beginner"].get("description"):
        lines.append(roadmap["beginner"]["description"])
        lines.append("")

    lines.append("---")
    lines.append("")

    

    for level_name, level in roadmap.items():

        lines.append(f"## {level_name.title()}")
        lines.append("")

        lines.append(level["description"])
        lines.append("")

        lines.append(
            f"**Estimated Duration:** {level['estimated_weeks']} weeks"
        )

        lines.append("")

       

        for concept in level["concepts"]:

            lines.append(f"### {concept['name']}")
            lines.append("")

            lines.append(f"- **Difficulty:** {concept['difficulty']}")
            lines.append(f"- **Priority:** {concept['priority']}")
            lines.append("")

            lines.append("#### Resources")
            lines.append("")

            for resource in concept["resources"]:

                icon = icons.get(resource["type"], "🔗")

                lines.append(
                    f"- {icon} [{resource['title']}]({resource['url']})"
                )

            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("Generated with The RoadMapper")

    return "\n".join(lines)


def roadmap_to_pdf(topic:str,roadmap:dict)->bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story=[]
    story.append(
        Paragraph(topic,styles["Title"])
    )
    story.append(
        Spacer(1,20)
    )

    for level_name,level in roadmap.items():
        story.append(
            Paragraph(level_name.title(),styles["Heading1"])
        )
        story.append(
            Paragraph(level["description"],styles["BodyText"])

        )
        story.append(
            Paragraph(
                f"<b>Estimated Duration:</b> {level["estimated_weeks"]} weeks",
                styles["BodyText"]
            )

        )

        story.append(Spacer(1,10))

        for concept in level["concepts"]:
            story.append(
                Paragraph(concept["name"], styles["Heading2"])
            )

            story.append(
                Paragraph(
                    f"<b>Difficulty:</b> {concept['difficulty']}",
                    styles["BodyText"],
                )
            )

            story.append(
                Paragraph(
                    f"<b>Priority:</b> {concept['priority']}",
                    styles["BodyText"],
                )
            )
            story.append(Spacer(1,5))
            story.append(
                Paragraph("<b>Resources</b>", styles["BodyText"])
            )

            for resource in concept["resources"]:

                story.append(
                    Paragraph(
                        f"• <a href='{resource['url']}' color='blue'>{resource['title']}</a> "
                        f"({resource['type'].title()})",
                        styles["BodyText"],
                    )
                )

            story.append(Spacer(1, 12))

        story.append(Spacer(1, 20))
        story.append(
        Paragraph(
            "<i>Generated with The RoadMapper</i>",
            styles["Italic"],
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf
