from pymongo import MongoClient
from bson.objectid import ObjectId

class MemoryService:
    def __init__(self, config):
        uri = config.get("memory", "uri")

        print("🔌 Connecting to MongoDB:", uri)

        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)

        # Force connection check
        self.client.admin.command("ping")

        self.db = self.client[config.get("memory", "db_name")]
        self.collection = self.db[config.get("memory", "collection")]

        print("✅ MongoDB Connected Successfully")

    # -----------------------------
    # SAVE MEMORY
    # -----------------------------
    def save(self, session_id: str, data: dict):
        try:
            print("💾 Saving data for:", session_id)

            doc = {
                "session_id": session_id,
                "data": data
            }

            result = self.collection.insert_one(doc)

            print("✅ Inserted ID:", str(result.inserted_id))

            return str(result.inserted_id)

        except Exception as e:
            print("❌ SAVE ERROR:", e)
            return None

    # -----------------------------
    # FETCH MEMORY (FIX FOR YOUR ERROR)
    # -----------------------------
    def fetch(self, session_id: str):
        try:
            print("📥 Fetching history for:", session_id)

            records = self.collection.find(
                {"session_id": session_id}
            ).sort("_id", 1)

            result = []

            for r in records:
                result.append({
                    "id": str(r.get("_id")),
                    "session_id": r.get("session_id"),
                    "data": r.get("data")
                })

            print(f"✅ Found {len(result)} records")

            return result

        except Exception as e:
            print("❌ FETCH ERROR:", e)
            return []

    # -----------------------------
    # OPTIONAL: CLEAR SESSION
    # -----------------------------
    def clear(self, session_id: str):
        try:
            result = self.collection.delete_many(
                {"session_id": session_id}
            )

            print(f"🧹 Deleted {result.deleted_count} records")

            return result.deleted_count

        except Exception as e:
            print("❌ DELETE ERROR:", e)
            return 0