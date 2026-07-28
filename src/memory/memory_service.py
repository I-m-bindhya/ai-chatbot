import sqlite3

class MemoryService:

    def __init__(self):
        self.connection = sqlite3.connect("src/database/chat.db", check_same_thread=False);
        self.cursor = self.connection.cursor();
        self.create_tables();

    def create_tables(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS conversations(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL)""")

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS summaries(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            conversation_id INTEGER NOT NULL UNIQUE,
                            summary TEXT NOT NULL,

                            FOREIGN KEY(conversation_id)
                            REFERENCES conversations(id)                            
                            )""")
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                            
                FOREIGN KEY(conversation_id)
                REFERENCES conversations(id)
            )
         """)
        self.connection.commit()

    def create_conversation(self, title = "New Chat"):
        self.cursor.execute("""
                            INSERT INTO conversations (title)
                            VALUES(?)""", (title,))
        self.connection.commit()
        conversation_id = self.cursor.lastrowid
        return conversation_id

    def update_conversation_title(self, conversation_id, title):
        self.cursor.execute("""
                            UPDATE conversations
                            SET title = ?
                            WHERE id = ?""", (title, conversation_id))
        self.connection.commit()
        print(
            "UPDATE TITLE",
            conversation_id,
            title
        )
        conversation_id = self.cursor.lastrowid
        return conversation_id
    
    def load_conversations(self):
        self.cursor.execute("""
                            SELECT id, title
                            FROM conversations
                            ORDER BY id
                            """)
        rows = self.cursor.fetchall()
        return rows

    def save_message(self, conversation_id, role, content):
        print("conversation id", conversation_id, role, content)
        self.cursor.execute("""
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?,?,?)
        """, (conversation_id, role, content))
        self.connection.commit()
        return self.cursor.lastrowid
        

    def load_messages(self, conversation_id):
        self.cursor.execute("""
            SELECT role, content 
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id
        """, (conversation_id,))
        rows = self.cursor.fetchall()
        message = []

        for role, content in rows:
            message.append({
                'role': role,
                'content': content
            })

        return message


    def clear_messages(self, conversation_id):
        self.cursor.execute("""
                            DELETE FROM conversations
                            WHERE id =?
                            """, (conversation_id,))
        self.connection.commit()
        self.cursor.execute("""
                        DELETE FROM messages
                        WHERE conversation_id = ?
                        """, (conversation_id,))
        self.connection.commit()


    def save_summary(
        self,
        conversation_id,
        summary
    ):
        self.cursor.execute("""
                INSERT INTO summaries (
                    conversation_id,
                    summary
                )
                VALUES (?, ?)
                ON CONFLICT(conversation_id)
                DO UPDATE SET
                summary = excluded.summary;
            """, (conversation_id, summary))

        self.connection.commit()
        summary_id  = self.cursor.fetchone()[0]
        return summary_id;
        

    def load_summary(
        self,
        conversation_id
    ):

        self.cursor.execute("""
                    SELECT id, summaries
                    FROM summary
                    WHERE conversation_id = ?
                    """, (conversation_id, ))
        rows = self.cursor.fetchall()
        return rows