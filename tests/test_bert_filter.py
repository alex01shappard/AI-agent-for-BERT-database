import unittest
from unittest.mock import patch, MagicMock
from bert_filter import BertFilter


class TestBertFilter(unittest.TestCase):
    @patch("bert_filter.BertTokenizer.from_pretrained")
    @patch("bert_filter.BertForSequenceClassification.from_pretrained")
    def test_classify_prompt(self, mock_model_cls, mock_tokenizer_cls):
        mock_tokenizer = MagicMock()
        mock_tokenizer_cls.return_value = mock_tokenizer

        mock_model = MagicMock()
        mock_model.eval = MagicMock()
        mock_model_cls.return_value = mock_model

        classifier = BertFilter(model_path="mock_path")
        classifier.model = MagicMock()
        classifier.model.eval = MagicMock()

        with (patch("torch.no_grad"),
              patch("torch.argmax",
                    return_value=MagicMock(item=MagicMock(return_value=1)))):
            result = classifier.classify_prompt("test prompt")
            self.assertEqual(result, 1)
