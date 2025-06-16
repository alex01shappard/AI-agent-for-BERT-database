import unittest
import sqlite3
import tempfile
import os
import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Создаём временный файл, закрываем сразу, чтобы не блокировал доступ
        self.temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db_file.close()

        database.DB_NAME = self.temp_db_file.name
        database.init_db()
        self.conn = sqlite3.connect(database.DB_NAME)
        self.cursor = self.conn.cursor()

    def test_init_db_creates_table(self):
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
            "AND name='prompts'")
        table = self.cursor.fetchone()
        self.assertIsNotNone(table)
        self.assertEqual(table[0], "prompts")

    def test_insert_prompt_inserts_data(self):
        database.insert_prompt("test prompt", 0)
        self.cursor.execute("SELECT prompt_text, label FROM prompts")
        rows = self.cursor.fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "test prompt")
        self.assertEqual(rows[0][1], 0)

    def tearDown(self):
        self.conn.close()
        os.unlink(self.temp_db_file.name)
