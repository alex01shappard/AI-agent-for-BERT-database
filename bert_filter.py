import torch
from transformers import BertTokenizer, BertForSequenceClassification


class BertFilter:
    def __init__(self, model_path="my_bert_model"):
        # Загружаем токенизатор и модель из указанной папки
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(
            model_path, num_labels=2)
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()  # Перевод модели в режим оценки

    def classify_prompt(self, prompt: str) -> int:
        """
        Классифицирует промпт:
          0 - Regular prompt
          1 - Jailbreak prompt
        """
        inputs = self.tokenizer(
            prompt,
            padding=True,
            truncation=True,
            return_tensors='pt',
            max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
            prediction = torch.argmax(outputs.logits, dim=-1).item()
        return prediction
