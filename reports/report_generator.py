import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)


# ============================================================
# SCHOLARSHIELD REPORT GENERATOR
# ============================================================

PROJECT_NAME = "ScholarShield"
PROJECT_SUBTITLE = "Context-Aware Academic Similarity Analyzer"


# ============================================================
# HELPERS
# ============================================================

def _safe_text(value, default="Not available"):
    """Convert a value to printable text safely."""
    if value is None:
        return default

    text = str(value).strip()

    return text if text else default


def _score(value):
    """Return a score as a percentage value."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _join_details(details):
    """
    Convert the NLP explanation 'details' list into readable text.
    The analysis page already stores these under:
    explanation -> component_explanations -> component -> details
    """
    if not isinstance(details, dict):
        return "No detailed explanation available."

    items = details.get("details", [])

    if isinstance(items, list):
        cleaned = [
            str(item).strip()
            for item in items
            if str(item).strip()
        ]

        if cleaned:
            return " ".join(cleaned)

    return "No detailed explanation available."


def _similarity_level(score):
    """Fallback interpretation if the NLP engine does not provide one."""
    score = _score(score)

    if score >= 80:
        return "Very High Similarity"
    if score >= 60:
        return "High Similarity"
    if score >= 40:
        return "Moderate Similarity"
    if score >= 20:
        return "Low Similarity"

    return "Very Low Similarity"


# ============================================================
# PAGE HEADER / FOOTER
# ============================================================

def _draw_header_footer(canvas, document):
    """Draw the ScholarShield header and page footer."""
    canvas.saveState()

    width, height = A4

    # Header
    canvas.setFillColor(colors.HexColor("#203F79"))
    canvas.rect(
        0,
        height - 8 * mm,
        width,
        8 * mm,
        stroke=0,
        fill=1,
    )

    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(colors.white)
    canvas.drawString(
        18 * mm,
        height - 5.3 * mm,
        PROJECT_NAME.upper(),
    )

    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(
        width - 18 * mm,
        height - 5.3 * mm,
        "Academic Similarity Analysis Report",
    )

    # Footer line
    canvas.setStrokeColor(colors.HexColor("#DCE3EE"))
    canvas.line(
        18 * mm,
        14 * mm,
        width - 18 * mm,
        14 * mm,
    )

    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#7A8798"))

    canvas.drawString(
        18 * mm,
        9 * mm,
        "ScholarShield - Context-Aware Academic Similarity Analyzer",
    )

    canvas.drawRightString(
        width - 18 * mm,
        9 * mm,
        f"Page {document.page}",
    )

    canvas.restoreState()


# ============================================================
# STYLES
# ============================================================

def _build_styles():
    styles = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=28,
            textColor=colors.HexColor("#14264A"),
            alignment=TA_LEFT,
            spaceAfter=5 * mm,
        ),

        "subtitle": ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#61718B"),
            spaceAfter=8 * mm,
        ),

        "section": ParagraphStyle(
            "Section",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#17294D"),
            spaceBefore=5 * mm,
            spaceAfter=3 * mm,
        ),

        "small_heading": ParagraphStyle(
            "SmallHeading",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#294064"),
            spaceAfter=2 * mm,
        ),

        "body": ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=14,
            textColor=colors.HexColor("#536176"),
            spaceAfter=3 * mm,
        ),

        "body_dark": ParagraphStyle(
            "BodyDark",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=14,
            textColor=colors.HexColor("#253A60"),
            spaceAfter=2 * mm,
        ),

        "label": ParagraphStyle(
            "Label",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#718099"),
            spaceAfter=1 * mm,
        ),

        "passage": ParagraphStyle(
            "Passage",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12.5,
            textColor=colors.HexColor("#536176"),
        ),

        "score": ParagraphStyle(
            "Score",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=19,
            textColor=colors.HexColor("#203F79"),
            alignment=TA_CENTER,
        ),

        "score_label": ParagraphStyle(
            "ScoreLabel",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#718099"),
            alignment=TA_CENTER,
        ),
    }


# ============================================================
# REPORT SECTIONS
# ============================================================

def _build_document_information(target_document, analysis_results, styles):
    target_name = _safe_text(
        target_document.get("filename"),
        "Target document",
    )

    reference_names = []

    for item in analysis_results:
        reference_document = item.get("reference_document", {})

        reference_names.append(
            _safe_text(
                reference_document.get("filename"),
                "Reference document",
            )
        )

    reference_text = "<br/>".join(
        f"• {name}" for name in reference_names
    )

    data = [
        [
            Paragraph("TARGET DOCUMENT", styles["label"]),
            Paragraph("REFERENCE DOCUMENTS", styles["label"]),
        ],
        [
            Paragraph(target_name, styles["body_dark"]),
            Paragraph(reference_text, styles["body_dark"]),
        ],
        [
            Paragraph("REPORT GENERATED", styles["label"]),
            Paragraph("ANALYSIS TYPE", styles["label"]),
        ],
        [
            Paragraph(
                datetime.now().strftime("%d %B %Y, %I:%M %p"),
                styles["body_dark"],
            ),
            Paragraph(
                "Context-aware multi-level similarity analysis",
                styles["body_dark"],
            ),
        ],
    ]

    table = Table(
        data,
        colWidths=[78 * mm, 100 * mm],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E0E6EF")),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E7ECF3")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F7F9FC")),
                ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#F7F9FC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    return table


def _build_score_table(result, styles):
    multi_level = result.get("multi_level", {})

    score_items = [
        ("Overall", multi_level.get("overall_score", 0)),
        ("Lexical", multi_level.get("lexical_score", 0)),
        ("Semantic", multi_level.get("semantic_score", 0)),
        ("Syntactic", multi_level.get("syntactic_score", 0)),
        ("Contextual", multi_level.get("contextual_score", 0)),
        ("Meaning", multi_level.get("meaning_score", 0)),
    ]

    cells = []

    for label, value in score_items:
        cells.append(
            [
                Paragraph(
                    f"{_score(value):.1f}%",
                    styles["score"],
                ),
                Paragraph(
                    label.upper(),
                    styles["score_label"],
                ),
            ]
        )

    table = Table(
        [cells],
        colWidths=[29.5 * mm] * 6,
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E0E6EF")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E7ECF3")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )

    return table


def _build_explanation_section(result, styles):
    explanation = result.get("explanation", {})

    simple_explanation = explanation.get(
        "simple_explanation",
        explanation.get("explanation", ""),
    )

    technical_explanation = explanation.get(
        "technical_explanation",
        "",
    )

    overall_interpretation = explanation.get(
        "overall_interpretation",
        "",
    )

    component_explanations = explanation.get(
        "component_explanations",
        {},
    )

    story = []

    if simple_explanation:
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "<b>Why these documents are similar</b>",
                            styles["small_heading"],
                        )
                    ],
                    [
                        Paragraph(
                            _safe_text(
                                simple_explanation,
                                "No plain-language explanation available.",
                            ),
                            styles["body"],
                        )
                    ],
                ],
                colWidths=[178 * mm],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFF")),
                        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E0E6EF")),
                        ("LEFTPADDING", (0, 0), (-1, -1), 10),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ]
                ),
            )
        )

        story.append(Spacer(1, 4 * mm))

    if technical_explanation:
        story.append(
            Paragraph(
                "Technical Explanation",
                styles["small_heading"],
            )
        )
        story.append(
            Paragraph(
                technical_explanation,
                styles["body"],
            )
        )

    if overall_interpretation:
        story.append(
            Paragraph(
                f"<b>Overall interpretation:</b> "
                f"{overall_interpretation}",
                styles["body"],
            )
        )

    story.append(
        Paragraph(
            "NLP Component Breakdown",
            styles["small_heading"],
        )
    )

    rows = [
        [
            Paragraph("COMPONENT", styles["label"]),
            Paragraph("SCORE", styles["label"]),
            Paragraph("CONTRIBUTION", styles["label"]),
        ]
    ]

    score_map = {
        "Lexical": result.get("multi_level", {}).get("lexical_score", 0),
        "Semantic": result.get("multi_level", {}).get("semantic_score", 0),
        "Syntactic": result.get("multi_level", {}).get("syntactic_score", 0),
        "Contextual": result.get("multi_level", {}).get("contextual_score", 0),
        "Meaning": result.get("multi_level", {}).get("meaning_score", 0),
    }

    component_keys = {
        "Lexical": "lexical",
        "Semantic": "semantic",
        "Syntactic": "syntactic",
        "Contextual": "contextual",
        "Meaning": "meaning",
    }

    for component, score in score_map.items():
        details = component_explanations.get(
            component_keys[component],
            {},
        )

        rows.append(
            [
                Paragraph(component, styles["body_dark"]),
                Paragraph(
                    f"{_score(score):.1f}%",
                    styles["body_dark"],
                ),
                Paragraph(
                    _join_details(details),
                    styles["body"],
                ),
            ]
        )

    table = Table(
        rows,
        colWidths=[30 * mm, 25 * mm, 123 * mm],
        repeatRows=1,
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5FB")),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E0E6EF")),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E7ECF3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(table)

    return story


def _build_similar_passages(result, styles):
    similar_passages = result.get("similar_passages", [])

    story = []

    if not similar_passages:
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "No highly similar passages were detected.",
                            styles["body"],
                        )
                    ]
                ],
                colWidths=[178 * mm],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFF")),
                        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E0E6EF")),
                        ("LEFTPADDING", (0, 0), (-1, -1), 10),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                    ]
                ),
            )
        )

        return story

    for index, match in enumerate(similar_passages, start=1):
        similarity_score = _score(
            match.get("similarity_score", 0)
        )

        target_sentence = _safe_text(
            match.get("target_sentence"),
            "Target passage unavailable.",
        )

        reference_sentence = _safe_text(
            match.get("reference_sentence"),
            "Reference passage unavailable.",
        )

        passage_table = Table(
            [
                [
                    Paragraph(
                        f"<b>MATCH {index}</b>",
                        styles["small_heading"],
                    ),
                    Paragraph(
                        f"<b>{similarity_score:.1f}% similarity</b>",
                        styles["body_dark"],
                    ),
                ],
                [
                    Paragraph(
                        "<b>Target Passage</b>",
                        styles["label"],
                    ),
                    Paragraph(
                        "<b>Reference Passage</b>",
                        styles["label"],
                    ),
                ],
                [
                    Paragraph(target_sentence, styles["passage"]),
                    Paragraph(reference_sentence, styles["passage"]),
                ],
            ],
            colWidths=[88 * mm, 88 * mm],
            hAlign="LEFT",
        )

        passage_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F7F9FC")),
                    ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FBFCFE")),
                    ("BACKGROUND", (0, 2), (-1, 2), colors.white),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E0E6EF")),
                    ("INNERGRID", (0, 1), (-1, -1), 0.4, colors.HexColor("#E7ECF3")),
                    ("SPAN", (0, 0), (0, 0)),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )

        story.append(
            KeepTogether(
                [
                    passage_table,
                    Spacer(1, 3 * mm),
                ]
            )
        )

    return story


# ============================================================
# PUBLIC REPORT FUNCTION
# ============================================================

def generate_analysis_report(
    target_document,
    analysis_results,
    output_path=None,
):

        # Convert SQLite Row objects to normal dictionaries
    if hasattr(target_document, "keys"):
        target_document = dict(target_document)

    normalized_results = []

    for analysis_item in analysis_results:

        item = dict(analysis_item)

        reference_document = item.get(
            "reference_document"
        )

        if hasattr(reference_document, "keys"):
            item["reference_document"] = dict(
                reference_document
            )

        normalized_results.append(item)

    analysis_results = normalized_results
    
    """
    Generate a ScholarShield PDF analysis report.

    Parameters
    ----------
    target_document : dict
        The target document dictionary used by analysis.py.
        Expected to contain at least 'filename'.

    analysis_results : list
        The exact list stored by analysis.py in:
        st.session_state["analysis_results"]

        Each item has:
            {
                "reference_document": {...},
                "result": {...}
            }

    output_path : str, optional
        Full path where the PDF should be created.

    Returns
    -------
    str
        The generated PDF file path.
    """

    if not target_document:
        raise ValueError("Target document is required.")

    if not analysis_results:
        raise ValueError("At least one analysis result is required.")

    if output_path is None:
        safe_name = os.path.splitext(
            _safe_text(
                target_document.get("filename"),
                "analysis_report",
            )
        )[0]

        safe_name = "".join(
            character
            if character.isalnum() or character in ("-", "_")
            else "_"
            for character in safe_name
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_path = os.path.join(
            "storage",
            "generated_reports",
            f"{safe_name}_analysis_{timestamp}.pdf",
        )

    output_path = os.path.abspath(output_path)

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True,
    )

    styles = _build_styles()

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=20 * mm,
        bottomMargin=19 * mm,
        title=f"{PROJECT_NAME} Analysis Report",
        author=PROJECT_NAME,
        subject=PROJECT_SUBTITLE,
    )

    story = []

    # --------------------------------------------------------
    # COVER / TITLE
    # --------------------------------------------------------

    story.append(Spacer(1, 7 * mm))

    story.append(
        Paragraph(
            "Academic Similarity Analysis Report",
            styles["title"],
        )
    )

    story.append(
        Paragraph(
            PROJECT_SUBTITLE
            + "<br/>"
            + "An explainable, context-aware comparison of academic documents.",
            styles["subtitle"],
        )
    )

    story.append(
        _build_document_information(
            target_document,
            analysis_results,
            styles,
        )
    )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    for result_index, analysis_item in enumerate(
        analysis_results,
        start=1,
    ):
        reference_document = analysis_item.get(
            "reference_document",
            {},
        )

        result = analysis_item.get(
            "result",
            {},
        )

        multi_level = result.get(
            "multi_level",
            {},
        )

        overall_score = _score(
            multi_level.get("overall_score", 0)
        )

        similarity_level = _safe_text(
            multi_level.get("similarity_level"),
            _similarity_level(overall_score),
        )

        reference_name = _safe_text(
            reference_document.get("filename"),
            "Reference document",
        )

        story.append(
            Paragraph(
                f"Reference Analysis {result_index}: "
                f"{reference_name}",
                styles["section"],
            )
        )

        # Overall result banner
        overall_table = Table(
            [
                [
                    Paragraph(
                        "<b>OVERALL SIMILARITY</b>",
                        styles["label"],
                    ),
                    Paragraph(
                        f"{overall_score:.1f}%",
                        styles["score"],
                    ),
                    Paragraph(
                        f"<b>{similarity_level}</b>",
                        styles["body_dark"],
                    ),
                ]
            ],
            colWidths=[55 * mm, 42 * mm, 81 * mm],
            hAlign="LEFT",
        )

        overall_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5FB")),
                    ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#D9E2F0")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (1, 0), (1, 0), "CENTER"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 9),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                    ("TOPPADDING", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                ]
            )
        )

        story.append(overall_table)
        story.append(Spacer(1, 4 * mm))

        # Multi-level scores
        story.append(
            Paragraph(
                "Multi-Level Similarity Scores",
                styles["small_heading"],
            )
        )

        story.append(
            _build_score_table(
                result,
                styles,
            )
        )

        # Explanations
        story.append(
            Paragraph(
                "Similarity Explanation",
                styles["section"],
            )
        )

        story.extend(
            _build_explanation_section(
                result,
                styles,
            )
        )

        # Similar passages
        story.append(
            Paragraph(
                "Similar Passages",
                styles["section"],
            )
        )

        story.append(
            Paragraph(
                "Sentences identified as meaningfully similar between "
                "the target and reference document.",
                styles["body"],
            )
        )

        story.extend(
            _build_similar_passages(
                result,
                styles,
            )
        )

        if result_index < len(analysis_results):
            story.append(PageBreak())

    # --------------------------------------------------------
    # REPORT NOTE
    # --------------------------------------------------------

    story.append(Spacer(1, 5 * mm))

    story.append(
        Table(
            [
                [
                    Paragraph(
                        "<b>ScholarShield interpretation note</b><br/>"
                        "This report presents linguistic similarity findings "
                        "across lexical, semantic, syntactic, contextual and "
                        "meaning-oriented dimensions. Similarity scores are "
                        "analytical indicators and should not be treated as "
                        "a definitive determination of plagiarism.",
                        styles["body"],
                    )
                ]
            ],
            colWidths=[178 * mm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFF")),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#DCE6F4")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                ]
            ),
        )
    )

    document.build(
        story,
        onFirstPage=_draw_header_footer,
        onLaterPages=_draw_header_footer,
    )

    return output_path
