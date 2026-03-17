"""
Script to create all CSV files with sample data
"""

import pandas as pd
from pathlib import Path
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Create data directory
data_dir = Path(__file__).parent / "data" / "csv"
data_dir.mkdir(parents=True, exist_ok=True)

# Users CSV
users_data = {
    "user_id": ["USR001", "USR002", "USR003", "USR004", "USR005"],
    "username": ["admin", "DebK", "priya_sharma", "amit_roy", "sarah_wilson"],
    "email": ["admin@genlearn.ai", "debk@example.com", "priya@example.com", "amit@example.com", "sarah@example.com"],
    "password_hash": ["$2b$12$LLQK3hVmGBg6Wy1mZdGyNOn2ka67iR6Q4xE55.unhivXbxaPpe26i"] * 5,
    "role": ["admin", "user", "user", "user", "user"],
    "display_name": ["Administrator", "DebK", "Priya Sharma", "Amit Roy", "Sarah Wilson"],
    "avatar_id": ["", "AVT001", "AVT002", "AVT003", ""],
    "language_preference": ["en", "en", "hi", "bn", "en"],
    "voice_preference": ["female", "male", "female", "male", "female"],
    "full_vocal_mode": [False, False, False, True, False],
    "xp_points": [0, 2450, 1820, 980, 3200],
    "level": [1, 7, 5, 3, 9],
    "streak_days": [0, 12, 8, 3, 25],
    "created_at": ["2024-01-01T00:00:00", "2024-01-05T00:00:00", "2024-01-08T00:00:00", "2024-01-10T00:00:00", "2024-01-02T00:00:00"],
    "last_login": ["2024-01-15T10:30:00", "2024-01-15T09:00:00", "2024-01-14T18:45:00", "2024-01-15T11:20:00", "2024-01-15T08:15:00"]
}
pd.DataFrame(users_data).to_csv(data_dir / "users.csv", index=False)
print("✓ Created users.csv")

# Sessions CSV
sessions_data = {
    "session_id": ["SES001", "SES002", "SES003"],
    "user_id": ["USR002", "USR003", "USR004"],
    "topic": ["Photosynthesis", "Indian History", "Python Basics"],
    "difficulty_level": [5, 4, 3],
    "duration_minutes": [15, 20, 10],
    "visual_style": ["cartoon", "realistic", "cartoon"],
    "play_mode": ["solo", "solo", "team"],
    "team_id": ["", "", "TM001"],
    "tournament_id": ["", "", ""],
    "status": ["completed", "in_progress", "completed"],
    "current_cycle": [3, 2, 2],
    "total_cycles": [3, 4, 2],
    "score": [450, 280, 320],
    "started_at": ["2024-01-15T09:00:00", "2024-01-15T18:00:00", "2024-01-14T14:00:00"],
    "completed_at": ["2024-01-15T09:18:00", "", "2024-01-14T14:12:00"]
}
pd.DataFrame(sessions_data).to_csv(data_dir / "sessions.csv", index=False)
print("✓ Created sessions.csv")

# Scores CSV
scores_data = {
    "score_id": ["SCR001", "SCR002", "SCR003"],
    "user_id": ["USR002", "USR002", "USR002"],
    "session_id": ["SES001", "SES001", "SES001"],
    "question_id": ["Q001", "Q002", "DQ001"],
    "question_type": ["mcq", "mcq", "descriptive"],
    "user_answer": ["B", "A", "Plants use sunlight to make food through chlorophyll"],
    "is_correct": [True, False, True],
    "points_earned": [10, 2, 8],
    "time_taken_seconds": [8, 12, 45],
    "evaluated_at": ["2024-01-15T09:05:00", "2024-01-15T09:06:00", "2024-01-15T09:10:00"]
}
pd.DataFrame(scores_data).to_csv(data_dir / "scores.csv", index=False)
print("✓ Created scores.csv")

# MCQ Questions CSV
mcq_questions_data = {
    "question_id": ["Q001", "Q002", "Q003", "Q004", "Q005"],
    "topic": ["Photosynthesis", "Photosynthesis", "Python Basics", "Indian History", "Mathematics"],
    "difficulty_level": [5, 5, 3, 4, 6],
    "question_text": [
        "What is the primary pigment involved in photosynthesis?",
        "Where does photosynthesis primarily occur in a plant cell?",
        "What keyword is used to define a function in Python?",
        "Who was the first Prime Minister of India?",
        "What is the value of pi to 2 decimal places?"
    ],
    "option_a": ["Melanin", "Nucleus", "function", "Mahatma Gandhi", "3.12"],
    "option_b": ["Chlorophyll", "Mitochondria", "def", "Jawaharlal Nehru", "3.14"],
    "option_c": ["Hemoglobin", "Chloroplast", "func", "Sardar Patel", "3.16"],
    "option_d": ["Carotene", "Cell membrane", "define", "Subhas Chandra Bose", "3.18"],
    "correct_answer": ["B", "C", "B", "B", "B"],
    "explanation": [
        "Chlorophyll is the green pigment that captures light energy for photosynthesis.",
        "Chloroplasts contain chlorophyll and are the site of photosynthesis.",
        "The 'def' keyword is used to define functions in Python.",
        "Jawaharlal Nehru was the first Prime Minister of India.",
        "Pi is approximately 3.14159, which rounds to 3.14."
    ],
    "created_by": ["admin"] * 5,
    "is_ai_generated": [False] * 5,
    "created_at": ["2024-01-01T00:00:00"] * 5
}
pd.DataFrame(mcq_questions_data).to_csv(data_dir / "questions_mcq.csv", index=False)
print("✓ Created questions_mcq.csv")

# Descriptive Questions CSV
descriptive_questions_data = {
    "question_id": ["DQ001", "DQ002", "DQ003"],
    "topic": ["Photosynthesis", "Python Basics", "Indian History"],
    "difficulty_level": [5, 3, 4],
    "question_text": [
        "Explain how photosynthesis helps maintain Earth's atmosphere.",
        "Explain the difference between a list and a tuple in Python.",
        "Describe the significance of the Indian Independence movement."
    ],
    "model_answer": [
        "Photosynthesis helps maintain Earth's atmosphere by absorbing carbon dioxide and releasing oxygen. Plants take in CO2 from the air and, using sunlight energy, convert it into glucose while releasing O2 as a byproduct. This process is essential for maintaining the oxygen levels needed by most living organisms and helps regulate atmospheric CO2 levels.",
        "Lists are mutable sequences in Python, meaning their contents can be changed after creation. Tuples are immutable sequences that cannot be modified once created. Lists use square brackets [] while tuples use parentheses (). Tuples are generally faster and use less memory than lists.",
        "The Indian Independence movement was a series of activities aimed at ending British colonial rule in India. It involved non-violent resistance, civil disobedience, and various political campaigns. The movement led to India gaining independence on August 15, 1947, and influenced similar movements worldwide."
    ],
    "keywords": [
        "carbon dioxide,oxygen,sunlight,glucose,atmosphere,plants",
        "mutable,immutable,list,tuple,brackets,parentheses",
        "British,colonial,independence,1947,Gandhi,non-violent"
    ],
    "max_score": [10, 10, 10],
    "created_by": ["admin"] * 3,
    "is_ai_generated": [False] * 3,
    "created_at": ["2024-01-01T00:00:00"] * 3
}
pd.DataFrame(descriptive_questions_data).to_csv(data_dir / "questions_descriptive.csv", index=False)
print("✓ Created questions_descriptive.csv")

# Tournaments CSV
tournaments_data = {
    "tournament_id": ["TRN001", "TRN002"],
    "name": ["Science Masters 2024", "Python Challenge"],
    "topic": ["General Science", "Python Programming"],
    "difficulty_level": [6, 5],
    "start_datetime": ["2024-01-20T10:00:00", "2024-01-18T14:00:00"],
    "end_datetime": ["2024-01-20T12:00:00", "2024-01-18T15:30:00"],
    "duration_minutes": [120, 90],
    "max_participants": [100, 50],
    "team_size_min": [1, 1],
    "team_size_max": [5, 3],
    "entry_type": ["free", "invite_only"],
    "status": ["upcoming", "active"],
    "prize_1st": ["Gold Badge + 500 XP", "500 XP"],
    "prize_2nd": ["Silver Badge + 300 XP", "300 XP"],
    "prize_3rd": ["Bronze Badge + 100 XP", "150 XP"],
    "created_by": ["USR001", "USR001"],
    "created_at": ["2024-01-10T00:00:00", "2024-01-08T00:00:00"]
}
pd.DataFrame(tournaments_data).to_csv(data_dir / "tournaments.csv", index=False)
print("✓ Created tournaments.csv")

# Teams CSV
teams_data = {
    "team_id": ["TM001", "TM002", "TM003"],
    "team_name": ["Science Stars", "Code Warriors", "Brain Squad"],
    "created_by": ["USR002", "USR005", "USR003"],
    "tournament_id": ["", "TRN002", ""],
    "total_score": [4500, 3200, 2800],
    "rank": [1, 2, 3],
    "created_at": ["2024-01-05T00:00:00", "2024-01-10T00:00:00", "2024-01-12T00:00:00"]
}
pd.DataFrame(teams_data).to_csv(data_dir / "teams.csv", index=False)
print("✓ Created teams.csv")

# Team Members CSV
team_members_data = {
    "membership_id": ["TM001_USR002", "TM001_USR003", "TM002_USR005", "TM002_USR002"],
    "team_id": ["TM001", "TM001", "TM002", "TM002"],
    "user_id": ["USR002", "USR003", "USR005", "USR002"],
    "role": ["leader", "member", "leader", "member"],
    "joined_at": ["2024-01-05T00:00:00", "2024-01-06T00:00:00", "2024-01-10T00:00:00", "2024-01-11T00:00:00"]
}
pd.DataFrame(team_members_data).to_csv(data_dir / "team_members.csv", index=False)
print("✓ Created team_members.csv")

# Avatars CSV
avatars_data = {
    "avatar_id": ["AVT001", "AVT002", "AVT003"],
    "user_id": ["USR002", "USR003", "USR004"],
    "name": ["Explorer Raj", "Curious Priya", "Thinker Amit"],
    "image_path": ["avatars/avt001.png", "avatars/avt002.png", "avatars/avt003.png"],
    "creation_method": ["upload", "draw", "gallery"],
    "style": ["cartoon", "cartoon", "realistic"],
    "created_at": ["2024-01-05T00:00:00", "2024-01-08T00:00:00", "2024-01-10T00:00:00"]
}
pd.DataFrame(avatars_data).to_csv(data_dir / "avatars.csv", index=False)
print("✓ Created avatars.csv")

# Characters CSV
characters_data = {
    "character_id": ["CHR001", "CHR002", "CHR003"],
    "user_id": ["USR002", "USR002", "USR003"],
    "name": ["Luna the Fairy", "Professor Oak", "Ganesha Guide"],
    "image_path": ["characters/chr001.png", "characters/chr002.png", "characters/chr003.png"],
    "creation_method": ["draw", "upload", "gallery"],
    "description": ["A magical fairy who loves science", "A wise old owl who teaches", "A friendly elephant companion"],
    "created_at": ["2024-01-06T00:00:00", "2024-01-07T00:00:00", "2024-01-09T00:00:00"]
}
pd.DataFrame(characters_data).to_csv(data_dir / "characters.csv", index=False)
print("✓ Created characters.csv")

# Learning History CSV
learning_history_data = {
    "history_id": ["HIS001", "HIS002", "HIS003"],
    "user_id": ["USR002", "USR002", "USR002"],
    "session_id": ["SES001", "SES001", "SES001"],
    "content_type": ["image", "image", "video"],
    "content_id": ["IMG001", "IMG002", "VID001"],
    "content_path": ["generated_images/ses001_img001.png", "generated_images/ses001_img002.png", "generated_videos/ses001_vid001.mp4"],
    "topic": ["Photosynthesis"] * 3,
    "viewed_at": ["2024-01-15T09:01:00", "2024-01-15T09:02:00", "2024-01-15T09:08:00"]
}
pd.DataFrame(learning_history_data).to_csv(data_dir / "learning_history.csv", index=False)
print("✓ Created learning_history.csv")

print("\n✅ All CSV files created successfully!")
print(f"📁 Location: {data_dir}")
