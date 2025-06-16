import torch
from langchain.llms.base import LLM
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from bert_filter import BertFilter
from database import init_db, insert_prompt


class LlamaLLM(LLM):
    max_seq_length: int = 2000
    load_in_4bit: bool = True
    dtype: any = None
    model_name: str = "unsloth/Llama-3.2-1B-Instruct"
    model: any = None
    tokenizer: any = None
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    class Config:
        extra = "allow"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.llama_model = AutoModelForCausalLM.from_pretrained(
            "unsloth/Llama-3.2-1B-Instruct")
        self.tokenizer = AutoTokenizer.from_pretrained(
            "unsloth/Llama-3.2-1B-Instruct")
        self.llama_generator = pipeline(
            'text-generation',
            model=self.llama_model,
            tokenizer=self.tokenizer)

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Убираем self.model.to(self.device) -
        # модель уже настроена на нужное устройство

    def generate_llama_response(self, prompt_input):
        """ Генерация ответа через Llama"""
        try:
            output = self.llama_generator(
                prompt_input,
                max_length=200,
                num_return_sequences=1
            )

            return output[0]['generated_text']
        except Exception as e:
            return f"Ошибка: {str(e)}"

    @property
    def _llm_type(self) -> str:
        return "LlamaLLM"

    def _call(self, prompt: str, stop: list = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        inputs = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            return_attention_mask=True
        ).to(self.device)

        # Перемещаем тензоры на нужное устройство
        attention_mask = inputs[1].to(self.device) if len(inputs) > 1 else None

        generated_ids = self.model.generate(
            input_ids=inputs,
            attention_mask=attention_mask,  # .unsqueeze(0),
            max_new_tokens=2000,
            use_cache=True,
            temperature=1.5,
            min_p=0.1
        )
        return self.tokenizer.decode(generated_ids[0],
                                     skip_special_tokens=True)


def process_prompt(prompt: str) -> int:
    bert_filter = BertFilter(model_path="my_bert_model")
    label = bert_filter.classify_prompt(prompt)
    insert_prompt(prompt, label)
    return label


def main():
    init_db()
    user_prompt = input("Введите ваш промпт: ")
    label = process_prompt(user_prompt)
    if label == 1:
        answer = """Промпт классифицирован как: Jailbreak prompt.
        Запрос отклонен"""
        return answer
    else:
        llm = LlamaLLM()
        answer = llm.generate_llama_response(prompt_input=user_prompt)
        return answer


def main_with_prompt(user_prompt: str):
    init_db()
    label = process_prompt(user_prompt)
    if label == 1:
        return "Промпт классифицирован как: Jailbreak prompt. Запрос отклонен"
    else:
        llm = LlamaLLM()
        return llm.generate_llama_response(prompt_input=user_prompt)


if __name__ == "__main__":
    main()
