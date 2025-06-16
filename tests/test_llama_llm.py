from agent import LlamaLLM
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestLlamaLLM(unittest.TestCase):

    @patch("agent.pipeline")
    @patch("agent.AutoTokenizer.from_pretrained")
    @patch("agent.AutoModelForCausalLM.from_pretrained")
    def test_generate_llama_response(self,
                                     mock_model_cls,
                                     mock_tokenizer_cls,
                                     mock_pipeline):
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()
        mock_model_cls.return_value = mock_model
        mock_tokenizer_cls.return_value = mock_tokenizer

        mock_generator = MagicMock()
        mock_generator.return_value = [{"generated_text": "response text"}]
        mock_pipeline.return_value = mock_generator

        llm = LlamaLLM()
        response = llm.generate_llama_response("some prompt")
        self.assertEqual(response, "response text")

    @patch("agent.pipeline")
    @patch("agent.AutoTokenizer.from_pretrained")
    @patch("agent.AutoModelForCausalLM.from_pretrained")
    def test_generate_llama_response_exception(self,
                                               mock_model_cls,
                                               mock_tokenizer_cls,
                                               mock_pipeline):
        mock_model_cls.return_value = MagicMock()
        mock_tokenizer_cls.return_value = MagicMock()

        mock_generator = MagicMock()
        mock_generator.side_effect = Exception("fail")
        mock_pipeline.return_value = mock_generator

        llm = LlamaLLM()

        response = llm.generate_llama_response("some prompt")
        self.assertTrue(response.startswith("Ошибка:"))


if __name__ == "__main__":
    unittest.main()
