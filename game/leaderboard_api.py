import json
import os
import random
import threading
import time
import uuid
from pathlib import Path

import requests


# =============================================================
# MAZEPAINT SUPABASE CONFIG
# =============================================================

DEFAULT_SUPABASE_URL = "https://bxqnjxwmvcjdlgovyemo.supabase.co"
DEFAULT_SUPABASE_KEY = "sb_publishable_7aDZmQH47Wj6TMz17Y4lZw_6_mMKXH0"


class LeaderboardAPI:

    def __init__(self):
        self.url = (
            os.getenv("MAZEPAINT_SUPABASE_URL")
            or DEFAULT_SUPABASE_URL
        ).strip().rstrip("/")

        self.key = (
            os.getenv("MAZEPAINT_SUPABASE_KEY")
            or DEFAULT_SUPABASE_KEY
        ).strip()

        self.session = requests.Session()
        self.session.headers.update(self._headers())

        # =====================================================
        # PLAYER FILE
        # =====================================================

        instance_id = os.getenv("MAZEPAINT_INSTANCE", "").strip()

        if instance_id:
            self.player_file = (
                Path.home()
                / f".mazepaint_player_{instance_id}.json"
            )
        else:
            self.player_file = (
                Path.home()
                / ".mazepaint_player.json"
            )

        self.player_id = self._get_player_id()
        self.username = self._get_username()

        # =====================================================
        # ONLINE / HEARTBEAT
        # =====================================================

        self.online = False

        self._heartbeat_stop = threading.Event()
        self._heartbeat_thread = None

        # =====================================================
        # CONNECTION TEST
        # =====================================================

        self.check_connection()

    # =========================================================
    # CONFIG / CONNECTION
    # =========================================================

    def is_configured(self):
        return bool(self.url and self.key)

    def check_connection(self):
        """
        Test the Supabase REST endpoint.
        """

        if not self.is_configured():
            self.online = False
            return False

        try:
            endpoint = f"{self.url}/rest/v1/leaderboard"

            response = self.session.get(
                endpoint,
                params={
                    "select": "player_id",
                    "limit": 1,
                },
                timeout=5,
            )

            self.online = response.ok

            if not response.ok:
                print(
                    "Supabase connection error:",
                    response.status_code,
                    response.text[:500],
                )

            return self.online

        except requests.RequestException as e:
            self.online = False
            print("Supabase connection error:", e)
            return False

    # =========================================================
    # PLAYER ID
    # =========================================================

    def _get_player_id(self):
        """
        Every installation gets one stable UUID.
        """

        data = {}

        if self.player_file.exists():
            try:
                with open(
                    self.player_file,
                    "r",
                    encoding="utf-8",
                ) as f:
                    data = json.load(f)

                old_id = str(
                    data.get("player_id", "")
                ).strip()

                try:
                    return str(uuid.UUID(old_id))

                except (ValueError, AttributeError):
                    pass

            except Exception:
                pass

        player_id = str(uuid.uuid4())

        self._save_player_data(
            player_id,
            str(data.get("username", "")).strip(),
        )

        return player_id

    # =========================================================
    # USERNAME
    # =========================================================

    def _get_username(self):
        if self.player_file.exists():
            try:
                with open(
                    self.player_file,
                    "r",
                    encoding="utf-8",
                ) as f:
                    data = json.load(f)

                return str(
                    data.get("username", "")
                ).strip()

            except Exception:
                pass

        return ""

    def has_username(self):
        return bool(self.username.strip())

    def get_username(self):
        return self.username

    def set_username(self, username):
        username = str(username).strip()

        if not username:
            return False

        self.username = username

        self._save_player_data(
            self.player_id,
            self.username,
        )

        # Register player in player_profiles.
        self.register_player()

        return True

    # =========================================================
    # LOCAL PLAYER DATA
    # =========================================================

    def _save_player_data(self, player_id, username):
        try:
            self.player_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with open(
                self.player_file,
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(
                    {
                        "player_id": str(player_id),
                        "username": str(username),
                    },
                    f,
                    indent=4,
                )

        except Exception as e:
            print("Player save error:", e)

    # =========================================================
    # HEADERS
    # =========================================================

    def _headers(self):
        return {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

    # =========================================================
    # GENERIC REQUEST
    # =========================================================

    def _request(self, method, endpoint, **kwargs):
        """
        Generic Supabase request wrapper.
        """

        if not self.is_configured():
            self.online = False
            return None

        kwargs.setdefault("timeout", 10)

        try:
            response = self.session.request(
                method,
                endpoint,
                **kwargs,
            )

            self.online = True

            return response

        except requests.RequestException as e:
            self.online = False

            print(
                "Supabase request error:",
                e,
            )

            return None

    # =========================================================
    # PLAYER REGISTRATION
    # =========================================================

    def register_player(self):
        """
        Register/update player identity.

        player_profiles is the source of truth for:
        - username
        - player_id
        - Chat player discovery
        """

        if (
            not self.is_configured()
            or not self.player_id
            or not self.username
        ):
            return False

        endpoint = (
            f"{self.url}/rest/v1/player_profiles"
        )

        data = {
            "player_id": self.player_id,
            "username": self.username,
        }

        headers = self._headers()

        headers["Prefer"] = (
            "resolution=merge-duplicates,"
            "return=minimal"
        )

        response = self._request(
            "POST",
            endpoint,
            headers=headers,
            json=data,
        )

        if response is not None and response.ok:
            return True

        if response is not None:
            print(
                "Player profile registration error:",
                response.status_code,
                response.text[:500],
            )

        return False

    # =========================================================
    # SUBMIT SCORE
    # =========================================================

    def submit_score(
        self,
        level,
        time_seconds,
        stars,
    ):
        """
        ثبت بهترین رکورد بازیکن برای هر Level.
    
        اولویت رکورد:
        1. ستاره بیشتر
        2. اگر ستاره برابر بود، زمان کمتر
        """
    
        if not self.is_configured():
            print("Leaderboard is not configured.")
            return False
    
        if not self.username:
            print("Leaderboard: username is empty.")
            return False
    
        try:
            level = int(level)
            time_seconds = float(time_seconds)
            stars = int(stars)
        except (ValueError, TypeError):
            print("Leaderboard: invalid score data.")
            return False
    
        endpoint = f"{self.url}/rest/v1/leaderboard"
    
        # ---------------------------------------------------------
        # اول رکورد فعلی این بازیکن برای این Level را پیدا می‌کنیم
        # ---------------------------------------------------------
    
        params = {
            "select": "id,player_id,username,level,time_seconds,stars",
            "player_id": f"eq.{self.player_id}",
            "level": f"eq.{level}",
            "limit": 1,
        }
    
        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )
    
        if response is None:
            return False
    
        if not response.ok:
            print(
                "Leaderboard check error:",
                response.status_code,
                response.text,
            )
            return False
    
        try:
            existing = response.json()
        except ValueError:
            existing = []
    
        # =========================================================
        # اگر رکورد قبلی وجود دارد
        # =========================================================
    
        if existing:
    
            old = existing[0]
    
            try:
                old_stars = int(old.get("stars", 0))
                old_time = float(
                    old.get("time_seconds", 999999)
                )
            except (ValueError, TypeError):
                old_stars = 0
                old_time = 999999
    
            # -----------------------------------------------------
            # بررسی اینکه رکورد جدید بهتر هست یا نه
            # -----------------------------------------------------
    
            is_better = (
                stars > old_stars
                or (
                    stars == old_stars
                    and time_seconds < old_time
                )
            )
    
            # -----------------------------------------------------
            # رکورد جدید بهتر نیست
            # -----------------------------------------------------
    
            if not is_better:
                print(
                    f"Score ignored: "
                    f"old={old_stars}⭐/{old_time:.2f}s "
                    f"new={stars}⭐/{time_seconds:.2f}s"
                )
                return True
    
            # -----------------------------------------------------
            # رکورد جدید بهتر است → UPDATE
            # -----------------------------------------------------
    
            record_id = old.get("id")
    
            update_endpoint = endpoint
    
            update_params = {
                "id": f"eq.{record_id}",
            }
    
            update_data = {
                "player_id": self.player_id,
                "username": self.username,
                "level": level,
                "time_seconds": time_seconds,
                "stars": stars,
            }
    
            headers = self._headers()
            headers["Prefer"] = "return=minimal"
    
            update_response = self._request(
                "PATCH",
                update_endpoint,
                headers=headers,
                params=update_params,
                json=update_data,
            )
    
            if (
                update_response is not None
                and update_response.ok
            ):
                print(
                    f"New best score! "
                    f"Level {level}: "
                    f"{stars}⭐ / {time_seconds:.2f}s"
                )
                return True
    
            if update_response is not None:
                print(
                    "Leaderboard update error:",
                    update_response.status_code,
                    update_response.text,
                )
    
            return False
    
        # =========================================================
        # رکوردی وجود ندارد → INSERT
        # =========================================================
    
        data = {
            "player_id": self.player_id,
            "username": self.username,
            "level": level,
            "time_seconds": time_seconds,
            "stars": stars,
        }
    
        headers = self._headers()
        headers["Prefer"] = "return=minimal"
    
        insert_response = self._request(
            "POST",
            endpoint,
            headers=headers,
            json=data,
        )
    
        if (
            insert_response is not None
            and insert_response.ok
        ):
            print(
                f"First score submitted! "
                f"Level {level}: "
                f"{stars}⭐ / {time_seconds:.2f}s"
            )
            return True
    
        if insert_response is not None:
            print(
                "Leaderboard insert error:",
                insert_response.status_code,
                insert_response.text,
            )
    
        return False
    # =========================================================
    # LEVEL SCORES
    # =========================================================

    def get_top_scores(
        self,
        level=None,
        limit=10,
    ):
        if not self.is_configured():
            return []

        endpoint = (
            f"{self.url}/rest/v1/leaderboard"
        )

        params = {
            "select": "*",
            "order": "time_seconds.asc",
            "limit": int(limit),
        }

        if level is not None:
            params["level"] = (
                f"eq.{int(level)}"
            )

        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )

        if response is not None and response.ok:
            try:
                return response.json()

            except ValueError:
                return []

        if response is not None:
            print(
                "Leaderboard fetch error:",
                response.status_code,
                response.text,
            )

        return []

    # =========================================================
    # MY ALL SCORES
    # =========================================================

    def get_my_scores(self):
        if not self.is_configured():
            return []

        endpoint = (
            f"{self.url}/rest/v1/leaderboard"
        )

        params = {
            "select": "*",
            "player_id": (
                f"eq.{self.player_id}"
            ),
            "order": (
                "level.asc,"
                "time_seconds.asc"
            ),
            "limit": 1000,
        }

        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )

        if response is not None and response.ok:
            try:
                return response.json()

            except ValueError:
                return []

        return []

    # =========================================================
    # BEST RECORDS
    # =========================================================

    def get_my_records(self):
        scores = self.get_my_scores()

        records = {}

        for score in scores:
            try:
                level = int(
                    score.get("level")
                )

                time_seconds = float(
                    score.get(
                        "time_seconds",
                        999999,
                    )
                )

                stars = int(
                    score.get(
                        "stars",
                        0,
                    )
                )

            except Exception:
                continue

            old = records.get(level)

            if old is None:
                records[level] = {
                    "level": level,
                    "time_seconds": time_seconds,
                    "stars": stars,
                }

            elif stars > old["stars"]:
                records[level] = {
                    "level": level,
                    "time_seconds": time_seconds,
                    "stars": stars,
                }

            elif (
                stars == old["stars"]
                and time_seconds
                < old["time_seconds"]
            ):
                records[level] = {
                    "level": level,
                    "time_seconds": time_seconds,
                    "stars": stars,
                }

        return records

    def get_my_best_score(self, level):
        return self.get_my_records().get(
            int(level)
        )

    # =========================================================
    # MY STATS
    # =========================================================

    def get_my_stats(self):
        records = self.get_my_records()

        completed = len(records)

        total_stars = sum(
            record["stars"]
            for record in records.values()
        )

        total_time = sum(
            record["time_seconds"]
            for record in records.values()
        )

        return {
            "completed": completed,
            "total_stars": total_stars,
            "total_time": total_time,
            "records": records,
        }

    # =========================================================
    # WORLD RANK
    # =========================================================

    def get_world_rank(self):
        if not self.is_configured():
            return None

        endpoint = (
            f"{self.url}/rest/v1/rpc/"
            "get_player_rank"
        )

        response = self._request(
            "POST",
            endpoint,
            headers=self._headers(),
            json={
                "target_player": self.player_id
            },
        )

        if response is None or not response.ok:
            if response is not None:
                print(
                    "World rank error:",
                    response.status_code,
                    response.text,
                )

            return None

        try:
            result = response.json()

            if isinstance(result, int):
                return result

            if (
                isinstance(result, list)
                and result
            ):
                try:
                    return int(result[0])
                except Exception:
                    pass

            if isinstance(result, dict):
                rank = result.get(
                    "world_rank"
                )

                if rank is not None:
                    return int(rank)

        except Exception:
            pass

        return None

    # =========================================================
    # CHAT - SEND MESSAGE
    # =========================================================

    def send_message(
        self,
        receiver_id,
        message,
    ):
        if not self.is_configured():
            print(
                "Chat is not configured."
            )
            return False

        receiver_id = str(
            receiver_id
        ).strip()

        message = str(
            message
        ).strip()

        if not receiver_id or not message:
            return False

        if receiver_id == self.player_id:
            print(
                "You cannot send a message "
                "to yourself."
            )
            return False

        # Receiver must be UUID.
        try:
            receiver_id = str(
                uuid.UUID(receiver_id)
            )

        except (
            ValueError,
            AttributeError,
        ):
            print(
                "Chat error: receiver_id "
                "must be a valid UUID:",
                receiver_id,
            )

            return False

        endpoint = (
            f"{self.url}/rest/v1/"
            "chat_messages"
        )

        data = {
            "sender_id": self.player_id,
            "receiver_id": receiver_id,
            "message": message,
        }

        headers = self._headers()

        headers["Prefer"] = (
            "return=representation"
        )

        response = self._request(
            "POST",
            endpoint,
            headers=headers,
            json=data,
        )

        if response is not None and response.ok:
            try:
                result = response.json()

                if (
                    isinstance(result, list)
                    and result
                ):
                    return result[0]

            except ValueError:
                pass

            return True

        if response is not None:
            print(
                "Send message error:",
                response.status_code,
                response.text,
            )

        return False

    # =========================================================
    # GET CHAT MESSAGES
    # =========================================================

    def get_messages(
        self,
        other_player_id,
        limit=100,
    ):
        if not self.is_configured():
            return []

        try:
            other_player_id = str(
                uuid.UUID(
                    str(other_player_id).strip()
                )
            )

        except (
            ValueError,
            AttributeError,
        ):
            print(
                "Get messages error: "
                "invalid UUID:",
                other_player_id,
            )

            return []

        endpoint = (
            f"{self.url}/rest/v1/"
            "chat_messages"
        )

        params = {
            "select": "*",
            "or": (
                "("
                f"and(sender_id.eq.{self.player_id},"
                f"receiver_id.eq.{other_player_id}),"
                f"and(sender_id.eq.{other_player_id},"
                f"receiver_id.eq.{self.player_id})"
                ")"
            ),
            "order": "created_at.asc",
            "limit": int(limit),
        }

        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )

        if response is not None and response.ok:
            try:
                return response.json()

            except ValueError:
                return []

        if response is not None:
            print(
                "Get messages error:",
                response.status_code,
                response.text,
            )

        return []

    # =========================================================
    # MARK MESSAGE AS READ
    # =========================================================

    def mark_message_read(
        self,
        message_id,
    ):
        if not self.is_configured():
            return False

        endpoint = (
            f"{self.url}/rest/v1/"
            "chat_messages"
        )

        params = {
            "id": f"eq.{message_id}",
            "receiver_id": (
                f"eq.{self.player_id}"
            ),
        }

        data = {
            "is_read": True
        }

        headers = self._headers()

        headers["Prefer"] = (
            "return=minimal"
        )

        response = self._request(
            "PATCH",
            endpoint,
            headers=headers,
            params=params,
            json=data,
        )

        return bool(
            response is not None
            and response.ok
        )

    # =========================================================
    # MARK CONVERSATION READ
    # =========================================================

    def mark_conversation_read(
        self,
        other_player_id,
    ):
        if not self.is_configured():
            return False

        try:
            other_player_id = str(
                uuid.UUID(
                    str(other_player_id).strip()
                )
            )

        except (
            ValueError,
            AttributeError,
        ):
            return False

        endpoint = (
            f"{self.url}/rest/v1/"
            "chat_messages"
        )

        params = {
            "sender_id": (
                f"eq.{other_player_id}"
            ),
            "receiver_id": (
                f"eq.{self.player_id}"
            ),
            "is_read": "eq.false",
        }

        headers = self._headers()

        headers["Prefer"] = (
            "return=minimal"
        )

        response = self._request(
            "PATCH",
            endpoint,
            headers=headers,
            params=params,
            json={
                "is_read": True
            },
        )

        return bool(
            response is not None
            and response.ok
        )

    # =========================================================
    # UNREAD MESSAGE COUNT
    # =========================================================

    def get_unread_count(self):
        if not self.is_configured():
            return 0

        endpoint = (
            f"{self.url}/rest/v1/"
            "chat_messages"
        )

        params = {
            "select": "id",
            "receiver_id": (
                f"eq.{self.player_id}"
            ),
            "is_read": "eq.false",
        }

        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )

        if response is not None and response.ok:
            try:
                return len(
                    response.json()
                )

            except ValueError:
                return 0

        return 0

    # =========================================================
    # GET CONVERSATIONS
    # =========================================================

    def get_conversations(
        self,
        limit=1000,
    ):
        if not self.is_configured():
            return []

        endpoint = (
            f"{self.url}/rest/v1/"
            "chat_messages"
        )

        params = {
            "select": "*",
            "or": (
                f"sender_id.eq.{self.player_id},"
                f"receiver_id.eq.{self.player_id}"
            ),
            "order": "created_at.desc",
            "limit": int(limit),
        }

        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )

        if response is None or not response.ok:
            if response is not None:
                print(
                    "Get conversations error:",
                    response.status_code,
                    response.text,
                )

            return []

        try:
            messages = response.json()

        except ValueError:
            return []

        conversations = {}

        for message in messages:
            sender = message.get(
                "sender_id"
            )

            receiver = message.get(
                "receiver_id"
            )

            other_id = (
                receiver
                if sender == self.player_id
                else sender
            )

            if (
                other_id
                and other_id not in conversations
            ):
                conversations[other_id] = message

        return list(
            conversations.values()
        )

    # =========================================================
    # FIND PLAYER BY USERNAME
    # =========================================================

    def find_player(self, username):
        if not self.is_configured():
            return None

        username = str(
            username
        ).strip()

        if not username:
            return None

        endpoint = (
            f"{self.url}/rest/v1/"
            "player_profiles"
        )

        params = {
            "select": "player_id,username",
            "username": f"eq.{username}",
            "player_id": (
                f"neq.{self.player_id}"
            ),
            "limit": 1,
        }

        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )

        if response is not None and response.ok:
            try:
                players = response.json()

                if players:
                    return players[0]

            except ValueError:
                pass

        if response is not None:
            print(
                "Find player error:",
                response.status_code,
                response.text[:500],
            )

        return None

    # =========================================================
    # GET PLAYER
    # =========================================================

    def get_player(
        self,
        player_id,
    ):
        if not self.is_configured():
            return None

        try:
            player_id = str(
                uuid.UUID(
                    str(player_id).strip()
                )
            )

        except (
            ValueError,
            AttributeError,
        ):
            return None

        endpoint = (
            f"{self.url}/rest/v1/"
            "player_profiles"
        )

        params = {
            "select": "player_id,username",
            "player_id": (
                f"eq.{player_id}"
            ),
            "limit": 1,
        }

        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )

        if response is not None and response.ok:
            try:
                players = response.json()

                if players:
                    return players[0]

            except ValueError:
                pass

        if response is not None:
            print(
                "Get player error:",
                response.status_code,
                response.text[:500],
            )

        return None

    # =========================================================
    # DISPLAY ID
    # =========================================================

    def get_display_id(
        self,
        player_id=None,
    ):
        if player_id is None:
            player_id = self.player_id

        raw_id = str(
            player_id
        ).encode("utf-8")

        import hashlib

        number = int(
            hashlib.sha256(
                raw_id
            ).hexdigest()[:12],
            16,
        )

        return f"{number % 100000:05d}"

    # =========================================================
    # SEARCH PLAYERS
    # =========================================================

    def search_players(
        self,
        query="",
        limit=30,
    ):
        if not self.is_configured():
            return []

        query = str(
            query
        ).strip()

        endpoint = (
            f"{self.url}/rest/v1/"
            "player_profiles"
        )

        params = {
            "select": "player_id,username",
            "player_id": (
                f"neq.{self.player_id}"
            ),
            "order": "username.asc",
            "limit": 1000,
        }

        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )

        if response is None or not response.ok:
            if response is not None:
                print(
                    "Search players error:",
                    response.status_code,
                    response.text[:500],
                )

            return []

        try:
            players = response.json()

        except ValueError:
            return []

        unique_players = {}

        for player in players:
            player_id = str(
                player.get(
                    "player_id",
                    "",
                )
            ).strip()

            username = str(
                player.get(
                    "username",
                    "",
                )
            ).strip()

            if not player_id or not username:
                continue

            if player_id == self.player_id:
                continue

            display_id = (
                self.get_display_id(
                    player_id
                )
            )

            if query:
                username_match = (
                    query.lower()
                    in username.lower()
                )

                id_match = (
                    query == display_id
                )

                if not (
                    username_match
                    or id_match
                ):
                    continue

            unique_players[player_id] = {
                "player_id": player_id,
                "username": username,
                "display_id": display_id,
            }

        return list(
            unique_players.values()
        )[:int(limit)]

    # =========================================================
    # ONLINE / HEARTBEAT
    # =========================================================

    def start_heartbeat(
        self,
        interval=30,
    ):
        """
        Starts a background heartbeat
        using player_presence.
        """

        if (
            self._heartbeat_thread
            and self._heartbeat_thread.is_alive()
        ):
            return True

        self._heartbeat_stop.clear()

        def loop():
            while not self._heartbeat_stop.is_set():
                self.update_online_status(
                    True
                )

                self._heartbeat_stop.wait(
                    max(
                        10,
                        int(interval),
                    )
                )

            self.update_online_status(
                False
            )

        self._heartbeat_thread = (
            threading.Thread(
                target=loop,
                daemon=True,
                name="MazePaint-Heartbeat",
            )
        )

        self._heartbeat_thread.start()

        return True

    def stop_heartbeat(self):
        self._heartbeat_stop.set()

    # =========================================================
    # UPDATE ONLINE STATUS
    # =========================================================

    def update_online_status(
        self,
        online=True,
    ):
        if (
            not self.is_configured()
            or not self.player_id
        ):
            return False

        endpoint = (
            f"{self.url}/rest/v1/"
            "player_presence"
        )

        data = {
            "player_id": self.player_id,
            "username": (
                self.username
                or "Player"
            ),
            "is_online": bool(online),
            "last_seen": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ",
                time.gmtime(),
            ),
        }

        headers = self._headers()

        headers["Prefer"] = (
            "resolution=merge-duplicates,"
            "return=minimal"
        )

        response = self._request(
            "POST",
            endpoint,
            headers=headers,
            json=data,
        )

        if response is not None and response.ok:
            return True

        if response is not None:
            print(
                "Presence update error:",
                response.status_code,
                response.text[:500],
            )

        return False

    # =========================================================
    # GET ONLINE PLAYERS
    # =========================================================


    def get_online_players(
        self,
        limit=100,
    ):
        if not self.is_configured():
            return []

        endpoint = (
            f"{self.url}/rest/v1/"
            "player_presence"
        )

        cutoff = time.strftime(
            "%Y-%m-%dT%H:%M:%SZ",
            time.gmtime(
                time.time() - 90
            ),
        )

        params = {
            "select": (
                "player_id,"
                "username,"
                "is_online,"
                "last_seen"
            ),
            "is_online": "eq.true",
            "last_seen": f"gte.{cutoff}",
            "player_id": (
                f"neq.{self.player_id}"
            ),
            "order": "last_seen.desc",
            "limit": int(limit),
        }

        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )

        if response is not None and response.ok:
            try:
                return response.json()

            except ValueError:
                return []

        return []



    def get_unread_message_count(self):
        if not self.is_configured() or not self.player_id:
            return 0

        endpoint = (
           f"{self.url}/rest/v1/"
           "chat_messages"
        )

        params = {
           "select": "id",
            "receiver_id": f"eq.{self.player_id}",
            "is_read": "eq.false",
        }

        response = self._request(
            "GET",
            endpoint,
            headers=self._headers(),
            params=params,
        )

        if response is not None and response.ok:
            try:
               return len(response.json())
            except ValueError:
               return 0

        return 0








