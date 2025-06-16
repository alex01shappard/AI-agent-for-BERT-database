import unittest
from unittest.mock import patch
from agent import main_with_prompt


class TestAgent(unittest.TestCase):

    @patch("agent.LlamaLLM")
    @patch("agent.process_prompt")
    @patch("agent.init_db")
    def test_main_with_prompt_jailbreak(self,
                                        mock_init_db,
                                        mock_process_prompt,
                                        mock_llama):
        mock_process_prompt.return_value = 1
        result = main_with_prompt("jailbreak prompt")
        self.assertEqual(
            result, "Промпт классифицирован как: Jailbreak prompt. "
            "Запрос отклонен")
        mock_llama.return_value.generate_llama_response.assert_not_called()

    @patch("agent.LlamaLLM")
    @patch("agent.process_prompt")
    @patch("agent.init_db")
    def test_main_with_prompt_regular(self,
                                      mock_init_db,
                                      mock_process_prompt,
                                      mock_llama):
        mock_process_prompt.return_value = 0
        mock_llama_instance = mock_llama.return_value
        mock_llama_instance.generate_llama_response.return_value = "regular "\
            "response"

        result = main_with_prompt("regular prompt")
        self.assertEqual(result, "regular response")
        mock_llama_instance.generate_llama_response.assert_called_once_with(
            prompt_input="regular prompt")


if __name__ == "__main__":
    unittest.main()
