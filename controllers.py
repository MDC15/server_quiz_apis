# controllers.py
import hashlib
from database import Database
from models import Player
import logging


class PlayerController:
    def __init__(self):
        self.db = Database()

    def create_id_hash(self, name: str) -> str:
        return hashlib.sha256(name.encode()).hexdigest()

    def submit_score(self, player: Player):
        try:
            conn = self.db.get_connection()
            id_hash = self.create_id_hash(player.name)

            existing_player = conn.execute(
                "SELECT * FROM players WHERE id_hash = ?", (id_hash,)
            ).fetchone()

            if existing_player:
                conn.execute(
                    "UPDATE players SET score = ?, time = ? WHERE id_hash = ?",
                    (player.score, player.time, id_hash),
                )
                message = "Score updated successfully"
                logging.info(f"Updated score for player: {player.name}")
            else:
                conn.execute(
                    "INSERT INTO players (id_hash, name, score, time) VALUES (?, ?, ?, ?)",
                    (id_hash, player.name, player.score, player.time),
                )
                message = "Score submitted successfully"
                logging.info(f"New player score submitted: {player.name}")

            conn.commit()
            return {"message": message}
        except Exception as e:
            logging.error(f"Error submitting score: {str(e)}")
            raise
        finally:
            conn.close()

    def get_ranking(self, limit=10):
        try:
            conn = self.db.get_connection()
            players = conn.execute(
                "SELECT name, score, time FROM players ORDER BY score DESC, time LIMIT ?",
                (limit,),
            ).fetchall()

            rankings = [
                {
                    "name": player["name"],
                    "score": player["score"],
                    "time": player["time"],
                }
                for player in players
            ]
            logging.info("Rankings retrieved successfully")
            return rankings
        except Exception as e:
            logging.error(f"Error getting rankings: {str(e)}")
            raise
        finally:
            conn.close()
