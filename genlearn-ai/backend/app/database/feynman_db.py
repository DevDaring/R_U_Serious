"""
CSV Database handlers for Feynman Engine
R U Serious? Application
"""

import os
import json
import uuid
import math
import pandas as pd
from datetime import datetime
from typing import Optional, List, Dict, Any


from app.config import settings


class FeynmanDatabase:
    """Handles all CSV operations for Feynman Engine"""
    
    def __init__(self):
        self.csv_dir = str(settings.CSV_DIR)
        self.sessions_path = os.path.join(self.csv_dir, 'feynman_sessions.csv')
        self.conversations_path = os.path.join(self.csv_dir, 'feynman_conversations.csv')
        self.gaps_path = os.path.join(self.csv_dir, 'feynman_gaps.csv')
        self.analogies_path = os.path.join(self.csv_dir, 'feynman_analogies.csv')
        self.users_path = os.path.join(self.csv_dir, 'users.csv')
        
        # Initialize CSVs if they don't exist
        self._initialize_csvs()
    
    def _initialize_csvs(self):
        """Create CSV files with headers if they don't exist"""
        
        # Ensure directory exists
        os.makedirs(self.csv_dir, exist_ok=True)
        
        if not os.path.exists(self.sessions_path):
            pd.DataFrame(columns=[
                'id', 'user_id', 'topic', 'subject', 'difficulty_level',
                'current_layer', 'started_at', 'completed_at', 'clarity_score',
                'compression_score', 'analogy_score', 'why_depth_reached',
                'gaps_discovered', 'teaching_xp_earned', 'status',
                'analogy_image_count', 'interactions_since_image'
            ]).to_csv(self.sessions_path, index=False)
        else:
            # Ensure new columns exist in existing CSV
            try:
                df = pd.read_csv(self.sessions_path)
                changed = False
                for col in ['analogy_image_count', 'interactions_since_image']:
                    if col not in df.columns:
                        df[col] = 0
                        changed = True
                if changed:
                    df.to_csv(self.sessions_path, index=False)
            except Exception:
                pass
        
        if not os.path.exists(self.conversations_path):
            pd.DataFrame(columns=[
                'id', 'session_id', 'layer', 'turn_number', 'role', 'message',
                'confusion_level', 'curiosity_level', 'question_type',
                'gap_detected', 'image_url', 'created_at'
            ]).to_csv(self.conversations_path, index=False)
        
        if not os.path.exists(self.gaps_path):
            pd.DataFrame(columns=[
                'id', 'session_id', 'user_id', 'gap_topic', 'gap_description',
                'layer_discovered', 'why_depth', 'resolved', 'linked_session_id',
                'discovered_at', 'resolved_at'
            ]).to_csv(self.gaps_path, index=False)
        
        if not os.path.exists(self.analogies_path):
            pd.DataFrame(columns=[
                'id', 'user_id', 'topic', 'subject', 'analogy_text',
                'stress_test_passed', 'community_rating', 'upvotes', 'downvotes',
                'times_used', 'is_featured', 'created_at', 'updated_at'
            ]).to_csv(self.analogies_path, index=False)
    
    # ============== SESSION OPERATIONS ==============
    
    def create_session(
        self,
        user_id: str,
        topic: str,
        subject: str,
        difficulty_level: int,
        starting_layer: int = 1
    ) -> Dict[str, Any]:
        """Create a new Feynman session"""
        
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        session = {
            'id': session_id,
            'user_id': user_id,
            'topic': topic,
            'subject': subject,
            'difficulty_level': difficulty_level,
            'current_layer': starting_layer,
            'started_at': now,
            'completed_at': '',
            'clarity_score': 0.0,
            'compression_score': 0.0,
            'analogy_score': 0.0,
            'why_depth_reached': 0,
            'gaps_discovered': '[]',
            'teaching_xp_earned': 0,
            'status': 'active'
        }
        
        df = pd.read_csv(self.sessions_path)
        df = pd.concat([df, pd.DataFrame([session])], ignore_index=True)
        df.to_csv(self.sessions_path, index=False)
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        try:
            df = pd.read_csv(self.sessions_path)
            session = df[df['id'] == session_id]
            
            if session.empty:
                return None
            
            result = session.iloc[0].to_dict()
            # Handle NaN values
            for key, value in result.items():
                if pd.isna(value):
                    result[key] = None if key != 'gaps_discovered' else '[]'
            return result
        except Exception as e:
            print(f"Error getting session: {e}")
            return None
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session fields"""
        try:
            df = pd.read_csv(self.sessions_path)
            idx = df[df['id'] == session_id].index
            
            if idx.empty:
                return False
            
            for key, value in updates.items():
                if key in df.columns:
                    df.loc[idx, key] = value
            
            df.to_csv(self.sessions_path, index=False)
            return True
        except Exception as e:
            print(f"Error updating session: {e}")
            return False
    
    def get_user_sessions(
        self, 
        user_id: str, 
        status: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get sessions for a user"""
        try:
            df = pd.read_csv(self.sessions_path)
            sessions = df[df['user_id'] == user_id]
            
            if status:
                sessions = sessions[sessions['status'] == status]
            
            sessions = sessions.sort_values('started_at', ascending=False).head(limit)
            return self._sanitize_records(sessions.to_dict('records'))
        except Exception as e:
            print(f"Error getting user sessions: {e}")
            return []
    
    # ============== CONVERSATION OPERATIONS ==============
    
    def add_conversation_turn(
        self,
        session_id: str,
        layer: int,
        role: str,
        message: str,
        confusion_level: Optional[float] = None,
        curiosity_level: Optional[float] = None,
        question_type: Optional[str] = None,
        gap_detected: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a conversation turn"""
        
        try:
            df = pd.read_csv(self.conversations_path)
            
            # Get next turn number for this session and layer
            session_turns = df[(df['session_id'] == session_id) & (df['layer'] == layer)]
            turn_number = len(session_turns) + 1
            
            turn = {
                'id': str(uuid.uuid4()),
                'session_id': session_id,
                'layer': layer,
                'turn_number': turn_number,
                'role': role,
                'message': message,
                'confusion_level': confusion_level if confusion_level is not None else '',
                'curiosity_level': curiosity_level if curiosity_level is not None else '',
                'question_type': question_type or '',
                'gap_detected': gap_detected or '',
                'image_url': image_url or '',
                'created_at': datetime.utcnow().isoformat()
            }
            
            df = pd.concat([df, pd.DataFrame([turn])], ignore_index=True)
            df.to_csv(self.conversations_path, index=False)
            
            return turn
        except Exception as e:
            print(f"Error adding conversation turn: {e}")
            return {}
    
    def get_conversation_history(
        self, 
        session_id: str, 
        layer: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        try:
            df = pd.read_csv(self.conversations_path)
            history = df[df['session_id'] == session_id]
            
            if layer is not None:
                history = history[history['layer'] == layer]
            
            history = history.sort_values(['layer', 'turn_number'])
            return self._sanitize_records(history.to_dict('records'))
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []

    def update_last_assistant_image(self, session_id: str, layer: int, image_url: str) -> bool:
        """Update the image_url on the most recent assistant turn for a session/layer"""
        try:
            df = pd.read_csv(self.conversations_path)
            mask = (df['session_id'] == session_id) & (df['layer'] == layer) & (df['role'] == 'assistant')
            matching = df[mask]
            if matching.empty:
                return False
            last_idx = matching.index[-1]
            df.at[last_idx, 'image_url'] = image_url
            df.to_csv(self.conversations_path, index=False)
            return True
        except Exception as e:
            print(f"Error updating conversation image: {e}")
            return False
    
    def _sanitize_records(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sanitize NaN values in records to make them JSON-serializable"""
        sanitized = []
        for record in records:
            clean_record = {}
            for key, value in record.items():
                # Handle NaN values
                if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                    clean_record[key] = None
                elif pd.isna(value):
                    clean_record[key] = None
                else:
                    clean_record[key] = value
            sanitized.append(clean_record)
        return sanitized
    
    # ============== GAP OPERATIONS ==============
    
    def add_gap(
        self,
        session_id: str,
        user_id: str,
        gap_topic: str,
        gap_description: str,
        layer_discovered: int,
        why_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """Add a knowledge gap"""
        
        try:
            gap = {
                'id': str(uuid.uuid4()),
                'session_id': session_id,
                'user_id': user_id,
                'gap_topic': gap_topic,
                'gap_description': gap_description,
                'layer_discovered': layer_discovered,
                'why_depth': why_depth if why_depth is not None else '',
                'resolved': False,
                'linked_session_id': '',
                'discovered_at': datetime.utcnow().isoformat(),
                'resolved_at': ''
            }
            
            df = pd.read_csv(self.gaps_path)
            df = pd.concat([df, pd.DataFrame([gap])], ignore_index=True)
            df.to_csv(self.gaps_path, index=False)
            
            # Update session's gaps_discovered
            session = self.get_session(session_id)
            if session:
                gaps = json.loads(session.get('gaps_discovered') or '[]')
                gaps.append(gap_topic)
                self.update_session(session_id, {'gaps_discovered': json.dumps(gaps)})
            
            return gap
        except Exception as e:
            print(f"Error adding gap: {e}")
            return {}
    
    def get_user_gaps(
        self, 
        user_id: str, 
        resolved: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """Get gaps for a user"""
        try:
            df = pd.read_csv(self.gaps_path)
            gaps = df[df['user_id'] == user_id]
            
            if resolved is not None:
                gaps = gaps[gaps['resolved'] == resolved]
            
            return self._sanitize_records(gaps.to_dict('records'))
        except Exception as e:
            print(f"Error getting user gaps: {e}")
            return []
    
    def get_session_gaps(self, session_id: str) -> List[Dict[str, Any]]:
        """Get gaps for a specific session"""
        try:
            df = pd.read_csv(self.gaps_path)
            gaps = df[df['session_id'] == session_id]
            return self._sanitize_records(gaps.to_dict('records'))
        except Exception:
            return []
    
    def resolve_gap(self, gap_id: str, linked_session_id: Optional[str] = None) -> bool:
        """Mark a gap as resolved"""
        try:
            df = pd.read_csv(self.gaps_path)
            idx = df[df['id'] == gap_id].index
            
            if idx.empty:
                return False
            
            df.loc[idx, 'resolved'] = True
            df.loc[idx, 'resolved_at'] = datetime.utcnow().isoformat()
            
            if linked_session_id:
                df.loc[idx, 'linked_session_id'] = linked_session_id
            
            df.to_csv(self.gaps_path, index=False)
            return True
        except Exception as e:
            print(f"Error resolving gap: {e}")
            return False
    
    # ============== ANALOGY OPERATIONS ==============
    
    def save_analogy(
        self,
        user_id: str,
        topic: str,
        subject: str,
        analogy_text: str,
        stress_test_passed: bool = False
    ) -> Dict[str, Any]:
        """Save a user-created analogy"""
        
        try:
            analogy = {
                'id': str(uuid.uuid4()),
                'user_id': user_id,
                'topic': topic,
                'subject': subject,
                'analogy_text': analogy_text,
                'stress_test_passed': stress_test_passed,
                'community_rating': 0.0,
                'upvotes': 0,
                'downvotes': 0,
                'times_used': 0,
                'is_featured': False,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            df = pd.read_csv(self.analogies_path)
            df = pd.concat([df, pd.DataFrame([analogy])], ignore_index=True)
            df.to_csv(self.analogies_path, index=False)
            
            return analogy
        except Exception as e:
            print(f"Error saving analogy: {e}")
            return {}
    
    def get_analogies(
        self,
        topic: Optional[str] = None,
        subject: Optional[str] = None,
        featured_only: bool = False,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get analogies with filters"""
        try:
            df = pd.read_csv(self.analogies_path)
            
            if topic:
                df = df[df['topic'].str.contains(topic, case=False, na=False)]
            
            if subject:
                df = df[df['subject'] == subject]
            
            if featured_only:
                df = df[df['is_featured'] == True]
            
            df = df.sort_values('community_rating', ascending=False).head(limit)
            return self._sanitize_records(df.to_dict('records'))
        except Exception as e:
            print(f"Error getting analogies: {e}")
            return []
    
    def vote_analogy(self, analogy_id: str, vote_type: str) -> bool:
        """Upvote or downvote an analogy"""
        try:
            df = pd.read_csv(self.analogies_path)
            idx = df[df['id'] == analogy_id].index
            
            if idx.empty:
                return False
            
            if vote_type == 'upvote':
                df.loc[idx, 'upvotes'] = df.loc[idx, 'upvotes'] + 1
            elif vote_type == 'downvote':
                df.loc[idx, 'downvotes'] = df.loc[idx, 'downvotes'] + 1
            
            # Recalculate rating
            upvotes = df.loc[idx, 'upvotes'].values[0]
            downvotes = df.loc[idx, 'downvotes'].values[0]
            total = upvotes + downvotes
            if total > 0:
                df.loc[idx, 'community_rating'] = (upvotes / total) * 5
            
            df.loc[idx, 'updated_at'] = datetime.utcnow().isoformat()
            df.to_csv(self.analogies_path, index=False)
            return True
        except Exception as e:
            print(f"Error voting analogy: {e}")
            return False
    
    # ============== USER XP INTEGRATION (GRACEFUL) ==============
    
    def update_user_xp(self, user_id: str, xp_to_add: int) -> bool:
        """Update user XP in users.csv (graceful - works if file doesn't exist)"""
        try:
            if not os.path.exists(self.users_path):
                print("users.csv not found - XP not synced (standalone mode)")
                return False
            
            df = pd.read_csv(self.users_path)
            idx = df[df['id'] == user_id].index
            
            if idx.empty:
                print(f"User {user_id} not found in users.csv - XP not synced")
                return False
            
            # Check if xp_points column exists
            if 'xp_points' in df.columns:
                current_xp = df.loc[idx, 'xp_points'].values[0]
                df.loc[idx, 'xp_points'] = current_xp + xp_to_add
                df.to_csv(self.users_path, index=False)
                return True
            else:
                print("xp_points column not found in users.csv")
                return False
        except Exception as e:
            print(f"Error updating user XP: {e}")
            return False


# Singleton instance
feynman_db = FeynmanDatabase()
