import sqlite3
import json
from pathlib import Path
import numpy as np


# =========================================================
# DATABASE LOCATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "scholarshield.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    """
    Create and return a connection to the ScholarShield
    SQLite database.
    """

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():
    """
    Create the required database tables if they do not
    already exist.
    """

    connection = get_connection()

    schema_path = DATABASE_DIR / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)

    connection.commit()
    connection.close()


# =========================================================
# GET ALL USER DOCUMENTS
# =========================================================

def get_user_documents(user_id):
    """
    Get all documents belonging to the logged-in user.

    This function is used by the Analysis page.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            file_type,
            file_path,
            file_size,
            word_count,
            character_count,
            sentence_count,
            uploaded_at,
            status
        FROM documents
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
        """,
        (user_id,)
    )

    documents = cursor.fetchall()

    conn.close()

    return documents


# =========================================================
# ADD DOCUMENT
# =========================================================

def add_document(
    user_id,
    filename,
    file_type,
    file_path,
    file_size,
    word_count,
    character_count,
    sentence_count
):
    """
    Add a newly uploaded document.

    Newly uploaded documents are placed into
    the Yet to Analyze collection.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # -------------------------------------------------
        # Add document
        # -------------------------------------------------

        cursor.execute(
            """
            INSERT INTO documents (
                user_id,
                filename,
                file_type,
                file_path,
                file_size,
                word_count,
                character_count,
                sentence_count,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                filename,
                file_type,
                file_path,
                file_size,
                word_count,
                character_count,
                sentence_count,
                "Not Analyzed"
            )
        )

        document_id = cursor.lastrowid

        # -------------------------------------------------
        # Add to Yet to Analyze
        # -------------------------------------------------

        cursor.execute(
            """
            INSERT INTO not_analyzed (
                document_id
            )
            VALUES (?)
            """,
            (document_id,)
        )

        conn.commit()

        return document_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# =========================================================
# GET "MY DOCUMENTS"
# =========================================================

def get_not_analyzed_documents(user_id):
    """
    Get documents that:

    1. Have not been analyzed as a target yet.
    2. Have NOT already been used as a reference.

    These documents belong in:

        Library → Yet to Analyze → My Documents
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            d.id,
            d.filename,
            d.file_type,
            d.file_path,
            d.file_size,
            d.word_count,
            d.character_count,
            d.sentence_count,
            d.uploaded_at,
            d.status,
            NULL AS used_against

        FROM documents d

        INNER JOIN not_analyzed n
            ON d.id = n.document_id

        WHERE d.user_id = ?

        AND NOT EXISTS (
            SELECT 1
            FROM analysis_references ar
            WHERE ar.reference_document_id = d.id
        )

        ORDER BY d.uploaded_at DESC
        """,
        (user_id,)
    )

    documents = cursor.fetchall()

    conn.close()

    return documents


# =========================================================
# GET "REFERENCE DOCUMENTS"
# =========================================================

def get_reference_documents(user_id):
    """
    Get documents that have been used as reference documents
    in completed analyses but have NOT yet been analyzed
    themselves as target documents.

    These documents belong in:

        Library → Yet to Analyze → Reference Documents
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            d.id,
            d.filename,
            d.file_type,
            d.file_path,
            d.file_size,
            d.word_count,
            d.character_count,
            d.sentence_count,
            d.uploaded_at,
            d.status,

            GROUP_CONCAT(
                target.filename,
                '|||'
            ) AS used_against

        FROM documents d

        INNER JOIN analysis_references ar
            ON d.id = ar.reference_document_id

        INNER JOIN analyzed a
            ON ar.analysis_id = a.id

        INNER JOIN documents target
            ON a.original_document_id = target.id

        WHERE d.user_id = ?

        AND NOT EXISTS (
            SELECT 1
            FROM analyzed analyzed_target
            WHERE analyzed_target.original_document_id = d.id
        )

        GROUP BY d.id

        ORDER BY d.uploaded_at DESC
        """,
        (user_id,)
    )

    documents = cursor.fetchall()

    conn.close()

    return documents


# =========================================================
# SAVE COMPLETED ANALYSIS
# =========================================================

def save_analysis(
    target_document_id,
    analysis_results,
    report_path
):
    """
    Save a completed analysis session, its reference documents,
    NLP results, and generated report.

    Everything is saved transactionally.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # -------------------------------------------------
        # 1. Create analyzed record
        # -------------------------------------------------

        cursor.execute(
            """
            INSERT INTO analyzed (
                original_document_id
            )
            VALUES (?)
            """,
            (target_document_id,)
        )

        analysis_id = cursor.lastrowid

        # -------------------------------------------------
        # 2. Save references + results
        # -------------------------------------------------

        for item in analysis_results:

            reference_document = item["reference_document"]

            reference_document_id = reference_document["id"]

            result = item["result"]

            multi_level = result.get(
                "multi_level",
                {}
            )

            explanation = result.get(
                "explanation",
                {}
            )

            similar_passages = result.get(
                "similar_passages",
                []
            )

            # ---------------------------------------------
            # Save reference relationship
            # ---------------------------------------------

            cursor.execute(
                """
                INSERT INTO analysis_references (
                    analysis_id,
                    reference_document_id
                )
                VALUES (?, ?)
                """,
                (
                    analysis_id,
                    reference_document_id
                )
            )

            # ---------------------------------------------
            # Save NLP result
            # ---------------------------------------------

            cursor.execute(
                """
                INSERT INTO analysis_results (
                    analysis_id,
                    reference_document_id,
                    lexical_score,
                    semantic_score,
                    syntactic_score,
                    contextual_score,
                    meaning_score,
                    overall_score,
                    similarity_level,
                    similar_passages,
                    explanation
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    analysis_id,
                    reference_document_id,

                    multi_level.get(
                        "lexical_score",
                        0
                    ),

                    multi_level.get(
                        "semantic_score",
                        0
                    ),

                    multi_level.get(
                        "syntactic_score",
                        0
                    ),

                    multi_level.get(
                        "contextual_score",
                        0
                    ),

                    multi_level.get(
                        "meaning_score",
                        0
                    ),

                    multi_level.get(
                        "overall_score",
                        0
                    ),

                    multi_level.get(
                        "similarity_level",
                        ""
                    ),

                    json.dumps(
                        similar_passages,
                        default=lambda value:
                            value.item()
                            if isinstance(
                                value,
                                np.generic
                            )
                            else str(value)
                    ),

                    json.dumps(
                        explanation,
                        default=lambda value:
                            value.item()
                            if isinstance(
                                value,
                                np.generic
                            )
                            else str(value)
                    )
                )
            )

        # -------------------------------------------------
        # 3. Save generated report
        # -------------------------------------------------

        report_name = Path(report_path).name

        cursor.execute(
            """
            INSERT INTO reports (
                analysis_id,
                report_name,
                report_path
            )
            VALUES (?, ?, ?)
            """,
            (
                analysis_id,
                report_name,
                report_path
            )
        )

        # -------------------------------------------------
        # 4. Remove target AND reference documents from
        #    the direct "My Documents" pool
        # -------------------------------------------------

        # Remove the analyzed target document
        cursor.execute(
            """
            DELETE FROM not_analyzed
            WHERE document_id = ?
            """,
            (target_document_id,)
        )

        # Remove every document that was used as a reference
        # from the direct "My Documents" pool.
        #
        # It is still eligible to appear under
        # "Reference Documents" and can still be selected
        # later as a target.
        reference_ids = [
            item["reference_document"]["id"]
            for item in analysis_results
        ]

        if reference_ids:

            placeholders = ",".join(
                "?" for _ in reference_ids
            )

            cursor.execute(
                f"""
                DELETE FROM not_analyzed
                WHERE document_id IN ({placeholders})
                """,
                reference_ids
            )

        # -------------------------------------------------
        # 5. Mark target as analyzed
        # -------------------------------------------------

        cursor.execute(
            """
            UPDATE documents
            SET status = ?
            WHERE id = ?
            """,
            (
                "Analyzed",
                target_document_id
            )
        )

        # -------------------------------------------------
        # 6. Commit everything
        # -------------------------------------------------

        conn.commit()

        return analysis_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

# =========================================================
# GET COMPLETED ANALYSES
# =========================================================

def get_analyzed_documents(user_id):
    """
    Get all completed analysis sessions belonging to the user.

    IMPORTANT:
    Each row represents ONE complete analysis session,
    regardless of how many reference documents were used.

    Returns:
        analysis_id
        original_document_id
        filename
        analysis_date
        reference_documents
        overall_score
        similarity_level
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            a.id AS analysis_id,
            a.original_document_id,
            target.filename,
            a.analysis_date,

            (
                SELECT GROUP_CONCAT(
                    reference_name,
                    '|||'
                )
                FROM (
                    SELECT DISTINCT
                        reference.filename AS reference_name
                    FROM analysis_references refs
                    INNER JOIN documents reference
                        ON refs.reference_document_id = reference.id
                    WHERE refs.analysis_id = a.id
                    ORDER BY reference.filename
                )
            ) AS reference_documents,

            (
                SELECT AVG(result.overall_score)
                FROM analysis_results result
                WHERE result.analysis_id = a.id
            ) AS overall_score,

            (
                SELECT result.similarity_level
                FROM analysis_results result
                WHERE result.analysis_id = a.id
                ORDER BY result.overall_score DESC
                LIMIT 1
            ) AS similarity_level

        FROM analyzed a

        INNER JOIN documents target
            ON a.original_document_id = target.id

        WHERE target.user_id = ?

        ORDER BY a.analysis_date DESC
        """,
        (user_id,)
    )

    analyses = cursor.fetchall()

    conn.close()

    return analyses

# =========================================================
# DASHBOARD STATISTICS
# =========================================================

def get_dashboard_stats(user_id):
    """
    Get dynamic statistics for the dashboard.

    Returns:
        total_documents
        total_analyses
        average_similarity
        highest_similarity
        lowest_similarity
    """

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------------------------------
    # Total uploaded documents
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*) AS total_documents
        FROM documents
        WHERE user_id = ?
        """,
        (user_id,)
    )

    total_documents = cursor.fetchone()["total_documents"]

    # -----------------------------------------------------
    # Analysis statistics
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT
            COUNT(DISTINCT a.id) AS total_analyses,
            AVG(ar.overall_score) AS average_similarity,
            MAX(ar.overall_score) AS highest_similarity,
            MIN(ar.overall_score) AS lowest_similarity

        FROM analyzed a

        INNER JOIN documents d
            ON a.original_document_id = d.id

        LEFT JOIN analysis_results ar
            ON a.id = ar.analysis_id

        WHERE d.user_id = ?
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return {
        "total_documents": row["total_analyses"] * 0 + total_documents,
        "total_analyses": row["total_analyses"] or 0,
        "average_similarity": row["average_similarity"],
        "highest_similarity": row["highest_similarity"],
        "lowest_similarity": row["lowest_similarity"],
    }


# =========================================================
# DASHBOARD SIMILARITY TREND
# =========================================================

def get_dashboard_similarity_trend(user_id, limit=7):
    """
    Get recent analysis sessions for the dashboard trend chart.

    Each point represents the average overall similarity
    for one completed analysis session.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            a.id AS analysis_id,
            a.analysis_date,
            AVG(ar.overall_score) AS overall_score

        FROM analyzed a

        INNER JOIN documents d
            ON a.original_document_id = d.id

        LEFT JOIN analysis_results ar
            ON a.id = ar.analysis_id

        WHERE d.user_id = ?

        GROUP BY
            a.id,
            a.analysis_date

        ORDER BY
            a.analysis_date DESC

        LIMIT ?
        """,
        (user_id, limit)
    )

    rows = cursor.fetchall()

    conn.close()

    # Reverse so the chart displays oldest → newest
    return list(reversed(rows))


# =========================================================
# DASHBOARD PENDING ANALYSES
# =========================================================

def get_pending_analysis_documents(user_id, limit=5):
    """
    Get documents belonging to the user that have not yet
    been analyzed as target documents.

    A document can still appear here even if it has previously
    been used as a reference document.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            d.id,
            d.filename,
            d.file_type,
            d.file_size,
            d.word_count,
            d.uploaded_at,
            d.status

        FROM documents d

        WHERE d.user_id = ?

        AND NOT EXISTS (
            SELECT 1
            FROM analyzed a
            WHERE a.original_document_id = d.id
        )

        ORDER BY
            d.uploaded_at DESC

        LIMIT ?
        """,
        (user_id, limit)
    )

    documents = cursor.fetchall()

    conn.close()

    return documents

# =========================================================
# GET USER PROFILE
# =========================================================

def get_user_profile(user_id):
    """
    Get basic profile information for the logged-in user.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    profile = cursor.fetchone()

    conn.close()

    return profile


# =========================================================
# GET USER PROFILE STATISTICS
# =========================================================

def get_user_profile_stats(user_id):
    """
    Get document and analysis statistics for the user's
    profile page.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------------------------------
    # DOCUMENT COUNT
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*) AS total_documents
        FROM documents
        WHERE user_id = ?
        """,
        (user_id,)
    )

    total_documents = cursor.fetchone()["total_documents"]

    # -----------------------------------------------------
    # ANALYSIS STATISTICS
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT
            COUNT(DISTINCT a.id) AS total_analyses,
            AVG(ar.overall_score) AS average_similarity
        FROM analyzed a

        INNER JOIN documents d
            ON a.original_document_id = d.id

        LEFT JOIN analysis_results ar
            ON a.id = ar.analysis_id

        WHERE d.user_id = ?
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return {
        "total_documents": total_documents or 0,
        "total_analyses": row["total_analyses"] or 0,
        "average_similarity": row["average_similarity"]
    }

# =========================================================
# GET COMPLETE ANALYSIS DETAILS
# =========================================================

def get_analysis_details(
    analysis_id,
    user_id
):
    """
    Get the complete stored information for one analysis.

    This does NOT run NLP again.

    It retrieves:
        - target document
        - reference documents
        - stored similarity scores
        - explanations
        - similar passages
        - generated report
    """

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------------------------------
    # TARGET DOCUMENT
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT
            a.id AS analysis_id,
            a.analysis_date,

            d.id AS document_id,
            d.filename,
            d.file_type,
            d.file_path,
            d.word_count,
            d.uploaded_at

        FROM analyzed a

        INNER JOIN documents d
            ON a.original_document_id = d.id

        WHERE a.id = ?
        AND d.user_id = ?
        """,
        (
            analysis_id,
            user_id
        )
    )

    target_document = cursor.fetchone()

    if not target_document:
        conn.close()
        return None

    # -----------------------------------------------------
    # REFERENCES + RESULTS
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT
            d.id AS reference_document_id,
            d.filename,
            d.file_type,
            d.file_path,
            d.word_count,

            r.lexical_score,
            r.semantic_score,
            r.syntactic_score,
            r.contextual_score,
            r.meaning_score,
            r.overall_score,
            r.similarity_level,

            r.similar_passages,
            r.explanation

        FROM analysis_references ar

        INNER JOIN documents d
            ON ar.reference_document_id = d.id

        LEFT JOIN analysis_results r
            ON ar.analysis_id = r.analysis_id
            AND ar.reference_document_id =
                r.reference_document_id

        WHERE ar.analysis_id = ?

        ORDER BY d.filename
        """,
        (analysis_id,)
    )

    results = cursor.fetchall()

    # -----------------------------------------------------
    # REPORT
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT
            id,
            report_name,
            report_path,
            generated_at

        FROM reports

        WHERE analysis_id = ?

        ORDER BY generated_at DESC

        LIMIT 1
        """,
        (analysis_id,)
    )

    report = cursor.fetchone()

    conn.close()

    return {
        "target": target_document,
        "results": results,
        "report": report
    }


# =========================================================
# TEST / INITIALIZATION
# =========================================================

if __name__ == "__main__":

    initialize_database()

    print(
        "ScholarShield database initialized successfully."
    )

    print(
        f"Database location: {DATABASE_PATH}"
    )