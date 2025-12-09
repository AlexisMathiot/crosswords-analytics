"""Generate test data for crosswords analytics."""

import hashlib
import random
import uuid
from datetime import datetime, timedelta
from urllib.parse import urlparse

import pymysql

# Database connection
DB_URL = "mysql+pymysql://crossword:password@localhost:3306/crossword_db"

# Sample grid data based on real structure
SAMPLE_GRID = {
    "version": "test-grid-1.0",
    "rows": 14,
    "cols": 9,
    "clues": [
        {
            "position": "A1",
            "words": [
                {"displayOrder": 0, "clueText": "ENVOÛTERONT", "startPosition": "B1", "direction": "down", "answer": "ENSORCELLERONT", "isSubscriberClue": True, "isLongClue": False},
                {"displayOrder": 1, "clueText": "SUJETTE À DES CRISES", "startPosition": "A2", "direction": "right", "answer": "ANGOISSEE", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "C1",
            "words": [
                {"displayOrder": 0, "clueText": "PRÉPOSITION", "startPosition": "D1", "direction": "down", "answer": "POUR", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "ON LE LANCE", "startPosition": "C2", "direction": "down", "answer": "GO", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "E1",
            "words": [
                {"displayOrder": 0, "clueText": "HANTÉE EN RUSSIE", "startPosition": "F1", "direction": "down", "answer": "ISBA", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "COMME LES MAISONS DE FILMS D'HORREUR", "startPosition": "E2", "direction": "down", "answer": "ISOLEES", "isSubscriberClue": False, "isLongClue": True},
            ],
        },
        {
            "position": "G1",
            "words": [
                {"displayOrder": 0, "clueText": "DÉBAUCHE D'ÉTUDIANTS", "startPosition": "H1", "direction": "down", "answer": "WEI", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "NARCISSA ET BELLATRIX", "startPosition": "G2", "direction": "down", "answer": "SORCIERES", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "I1",
            "words": [
                {"displayOrder": 0, "clueText": "FONT BOUH", "startPosition": "I2", "direction": "down", "answer": "ESPRITS", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "A3",
            "words": [
                {"displayOrder": 0, "clueText": "LIEU FAVORI DES FAITS DIVERS", "startPosition": "B3", "direction": "right", "answer": "SOUSBOIS", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "C4",
            "words": [
                {"displayOrder": 0, "clueText": "PAS YES", "startPosition": "A4", "direction": "right", "answer": "NO", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "DÉSINENCE VERBALE", "startPosition": "C5", "direction": "down", "answer": "ER", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "H4",
            "words": [
                {"displayOrder": 0, "clueText": "BRUIT TERRIFIANT", "startPosition": "D4", "direction": "right", "answer": "ROAR", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "A5",
            "words": [
                {"displayOrder": 0, "clueText": "UNE ÎLE", "startPosition": "B5", "direction": "right", "answer": "RE", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "IL A PEUR", "startPosition": "A6", "direction": "right", "answer": "ECRIE", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "D5",
            "words": [
                {"displayOrder": 0, "clueText": "FILS DE PRIAM", "startPosition": "D6", "direction": "down", "answer": "ISOS", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "F5",
            "words": [
                {"displayOrder": 0, "clueText": "C'EST UN CUIVRE", "startPosition": "G5", "direction": "right", "answer": "COR", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "F6",
            "words": [
                {"displayOrder": 0, "clueText": "PAS LÀ", "startPosition": "G6", "direction": "right", "answer": "ICI", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "APPROUVERONS VIRTUELLEMENT", "startPosition": "F7", "direction": "down", "answer": "LIKERONS", "isSubscriberClue": False, "isLongClue": True},
            ],
        },
        {
            "position": "A7",
            "words": [
                {"displayOrder": 0, "clueText": "AVANT NOUS", "startPosition": "A8", "direction": "right", "answer": "IL", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "C7",
            "words": [
                {"displayOrder": 0, "clueText": "ÉLITISTE", "startPosition": "D7", "direction": "right", "answer": "SELECT", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "C8",
            "words": [
                {"displayOrder": 0, "clueText": "ROI DES MORTS", "startPosition": "D8", "direction": "right", "answer": "OSIRIS", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "ALTER EGO", "startPosition": "C9", "direction": "down", "answer": "AVATAR", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "A9",
            "words": [
                {"displayOrder": 0, "clueText": "PAS MOTIVÉ", "startPosition": "B9", "direction": "right", "answer": "LAS", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "VOUS NE SERIEZ PAS LÀ SANS LUI", "startPosition": "A10", "direction": "right", "answer": "DEV", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "E9",
            "words": [
                {"displayOrder": 0, "clueText": "HANTÉE EN BRETAGNE", "startPosition": "F9", "direction": "right", "answer": "KER", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "MATIÈRE DE POUPÉE MALÉFIQUE", "startPosition": "E10", "direction": "down", "answer": "CIRE", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "I9",
            "words": [
                {"displayOrder": 0, "clueText": "PROTOCOLES OCCULTES", "startPosition": "I10", "direction": "down", "answer": "RITES", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "D10",
            "words": [
                {"displayOrder": 0, "clueText": "DÉFILÉ DE STARS", "startPosition": "E10", "direction": "right", "answer": "CESAR", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "A11",
            "words": [
                {"displayOrder": 0, "clueText": "ENLEVER", "startPosition": "B11", "direction": "right", "answer": "RAVIR", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "UN PEU COMME JACK", "startPosition": "A12", "direction": "right", "answer": "POTIRON", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "G11",
            "words": [
                {"displayOrder": 0, "clueText": "AVANT III", "startPosition": "H11", "direction": "right", "answer": "II", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "ON Y VOLE À NANTES", "startPosition": "G12", "direction": "down", "answer": "NTE", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "H12",
            "words": [
                {"displayOrder": 0, "clueText": "S'OPPOSE À INTERNET", "startPosition": "H13", "direction": "down", "answer": "RL", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "A13",
            "words": [
                {"displayOrder": 0, "clueText": "DANS LA BALEINE", "startPosition": "B13", "direction": "right", "answer": "NA", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "S'ALLUME EN NOVEMBRE", "startPosition": "A14", "direction": "right", "answer": "ATRE", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "D13",
            "words": [
                {"displayOrder": 0, "clueText": "SIX À ROME", "startPosition": "D11", "direction": "down", "answer": "VI", "isSubscriberClue": False, "isLongClue": False},
                {"displayOrder": 1, "clueText": "FRANCHIT LE SEUIL", "startPosition": "E13", "direction": "right", "answer": "ENTRE", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
        {
            "position": "E14",
            "words": [
                {"displayOrder": 0, "clueText": "CHASSEURS D'ESPRITS", "startPosition": "F14", "direction": "right", "answer": "SELS", "isSubscriberClue": False, "isLongClue": False},
            ],
        },
    ],
}


def parse_db_url(url: str) -> dict:
    """Parse database URL into connection parameters."""
    # Remove the mysql+pymysql:// prefix
    if url.startswith("mysql+pymysql://"):
        url = url.replace("mysql+pymysql://", "mysql://")

    parsed = urlparse(url)
    return {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 3306,
        "user": parsed.username or "root",
        "password": parsed.password or "",
        "database": parsed.path.lstrip("/") if parsed.path else "crossword_db",
    }


def create_test_grid(conn, grid_data: dict) -> tuple[int, str, int]:
    """Create a test grid with clues and words.

    Returns: (grid_id, version, total_words)
    """
    cursor = conn.cursor()

    # Insert grid
    cursor.execute(
        """
        INSERT INTO grids (version, grid_rows, grid_cols, is_active, is_archived, published_at, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            grid_data["version"],
            grid_data["rows"],
            grid_data["cols"],
            True,
            False,
            datetime.now(),
            datetime.now(),
        ),
    )
    grid_id = cursor.lastrowid

    total_words = 0

    # Insert clues and words
    for clue_data in grid_data["clues"]:
        cursor.execute(
            "INSERT INTO clues (grid_id, position) VALUES (%s, %s)",
            (grid_id, clue_data["position"]),
        )
        clue_id = cursor.lastrowid

        for word_data in clue_data["words"]:
            answer = word_data["answer"]
            answer_hash = hashlib.sha256(answer.encode()).hexdigest()
            # Simple "encryption" for test data (just base64 in real app)
            encrypted_answer = answer[::-1]  # Reverse as placeholder

            cursor.execute(
                """
                INSERT INTO words (clue_id, display_order, clue_text, start_position, direction,
                                   answer_hash, encrypted_answer, is_long_clue, is_subscriber_clue)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    clue_id,
                    word_data["displayOrder"],
                    word_data["clueText"],
                    word_data["startPosition"],
                    word_data["direction"],
                    answer_hash,
                    encrypted_answer,
                    word_data.get("isLongClue", False),
                    word_data.get("isSubscriberClue", False),
                ),
            )
            total_words += 1

    conn.commit()
    print(f"Created grid '{grid_data['version']}' (id={grid_id}) with {total_words} words")
    return grid_id, grid_data["version"], total_words


def generate_submissions(grid_id: int, num_submissions: int = 50, total_words: int = 30):
    """Generate realistic test submissions for a grid."""
    submissions = []

    for i in range(num_submissions):
        # Random completion metrics - use actual total_words from grid
        words_found = random.randint(int(total_words * 0.3), total_words)

        # Completion time (30 seconds to 2 hours)
        completion_time = random.randint(30, 7200)

        # Joker usage (30% chance)
        joker_used = random.random() < 0.3

        # Calculate scores
        correct_cells = random.randint(0, 200)
        base_score = correct_cells * 5.0

        # Time bonus (faster = better)
        time_bonus = max(0, (3600 - completion_time) / 10)

        # Joker penalty
        joker_penalty = 50.0 if joker_used else 0.0

        # Final score
        final_score = max(0, base_score + time_bonus - joker_penalty)

        # Submission date (last 30 days)
        days_ago = random.randint(0, 30)
        submitted_at = datetime.now() - timedelta(
            days=days_ago, hours=random.randint(0, 23)
        )

        submissions.append(
            {
                "id": str(uuid.uuid4()),
                "grid_id": grid_id,
                "correct_cells": correct_cells,
                "base_score": base_score,
                "time_bonus": time_bonus,
                "joker_penalty": joker_penalty,
                "final_score": final_score,
                "completion_time_seconds": completion_time,
                "words_found": words_found,
                "total_words": total_words,
                "joker_used": joker_used,
                "submitted_at": submitted_at,
            }
        )

    return submissions


def uuid_to_bin(uuid_str: str) -> bytes:
    """Convert UUID string to binary format for MySQL."""
    return uuid.UUID(uuid_str).bytes


def bin_to_uuid(binary: bytes) -> str:
    """Convert binary UUID from MySQL to string."""
    return str(uuid.UUID(bytes=binary))


def create_test_users(conn, num_users):
    """Create multiple test users."""
    cursor = conn.cursor()
    user_ids = []

    for i in range(num_users):
        user_id = str(uuid.uuid4())
        email = f"testuser{i}@example.com"
        pseudo = f"Player{i + 1}"[:24]  # Max 24 chars

        # Use INSERT IGNORE for MySQL (equivalent to ON CONFLICT DO NOTHING)
        cursor.execute(
            """
            INSERT IGNORE INTO users (id, email, pseudo, roles, password, is_verified, auth_provider, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                uuid_to_bin(user_id),
                email,
                pseudo,
                '["ROLE_USER"]',
                "$2y$13$hashedpassword",  # Dummy hashed password
                True,
                "local",
                datetime.now(),
                datetime.now(),
            ),
        )

        if cursor.rowcount > 0:
            user_ids.append(user_id)
        else:
            # User already exists, fetch their ID
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                user_ids.append(bin_to_uuid(result[0]))

    conn.commit()
    return user_ids


def insert_submissions(conn, submissions, user_ids):
    """Insert submissions into database."""
    cursor = conn.cursor()

    # Assign each submission to a different user (convert UUIDs to binary)
    values = [
        (
            uuid_to_bin(sub["id"]),
            uuid_to_bin(user_ids[i % len(user_ids)]),  # Cycle through users
            sub["grid_id"],
            sub["correct_cells"],
            sub["base_score"],
            sub["time_bonus"],
            sub["joker_penalty"],
            sub["final_score"],
            sub["completion_time_seconds"],
            sub["words_found"],
            sub["total_words"],
            sub["joker_used"],
            sub["submitted_at"],
        )
        for i, sub in enumerate(submissions)
    ]

    # Use executemany for batch insert in MySQL
    cursor.executemany(
        """
        INSERT INTO submission (
            id, user_id, grid_id, correct_cells, base_score, time_bonus,
            joker_penalty, final_score, completion_time_seconds,
            words_found, total_words, joker_used, submitted_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        values,
    )

    conn.commit()
    print(f"Inserted {len(submissions)} submissions")


def get_total_words_for_grid(conn, grid_id: int) -> int:
    """Get the total number of words for a grid."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT COUNT(*) FROM words w
        JOIN clues c ON w.clue_id = c.id
        WHERE c.grid_id = %s
        """,
        (grid_id,),
    )
    result = cursor.fetchone()
    return result[0] if result else 30  # Default to 30 if not found


def main():
    """Main function to generate test data."""
    print("Generating test data for Crosswords Analytics...")

    # Parse database URL and connect
    db_params = parse_db_url(DB_URL)
    conn = pymysql.connect(**db_params)

    try:
        cursor = conn.cursor()

        # Check available grids
        cursor.execute("SELECT id, version FROM grids ORDER BY id LIMIT 5")
        grids = cursor.fetchall()

        # Create test grid if none exist
        if not grids:
            print("No grids found, creating test grid...")
            grid_id, version, total_words = create_test_grid(conn, SAMPLE_GRID)
            grids = [(grid_id, version)]
        else:
            print(f"Found {len(grids)} existing grids")

        # Generate submissions for each grid
        for grid_id, version in grids:
            print(f"\nGenerating data for Grid {grid_id} (version: {version})...")

            # Get actual word count for this grid
            total_words = get_total_words_for_grid(conn, grid_id)
            print(f"Grid has {total_words} words")

            # Delete existing test submissions for this grid
            cursor.execute("DELETE FROM submission WHERE grid_id = %s", (grid_id,))
            conn.commit()

            # Generate submissions (2500 per grid for performance testing)
            num_submissions = 2500
            print(f"Generating {num_submissions} submissions...")
            submissions = generate_submissions(grid_id, num_submissions, total_words)

            # Create enough test users for these submissions
            print(f"Creating {num_submissions} test users...")
            user_ids = create_test_users(conn, num_submissions)
            print(f"Created {len(user_ids)} test users")

            # Insert submissions (in batches for better performance)
            print("Inserting submissions...")
            insert_submissions(conn, submissions, user_ids)

        print("\nTest data generation completed!")
        print("\nYou can now view the analytics dashboard with realistic data!")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
