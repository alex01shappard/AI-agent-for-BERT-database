import sqlite3
from datetime import datetime

DB_NAME = "prompts.db"


def init_db():
    """
    Инициализирует базу данных.
    Создает таблицу prompts, если она не существует.
    Таблица содержит:
      - id: первичный ключ
      - prompt_text: текст промпта
      - label: 0 (regular) или 1 (jailbreak)
      - timestamp: время записи
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_text TEXT NOT NULL,
            label INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def insert_prompt(prompt_text: str, label: int):
    """
    Вставляет новый промпт в таблицу.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO prompts (prompt_text, label, timestamp)
        VALUES (?, ?, ?)
    ''', (prompt_text, label, timestamp))
    conn.commit()
    conn.close()
