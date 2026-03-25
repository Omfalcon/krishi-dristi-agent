

import torch
from typing import List, Union
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit.processor import IndicProcessor


EN_INDIC_MODEL = "ai4bharat/indictrans2-en-indic-dist-200M"
INDIC_EN_MODEL = "ai4bharat/indictrans2-indic-en-dist-200M"


LANGUAGE_CODES = {
    "english": "eng_Latn",
    "hindi": "hin_Deva",
    "tamil": "tam_Taml",
    "telugu": "tel_Telu",
    "kannada": "kan_Knda",
    "malayalam": "mal_Mlym",
    "bengali": "ben_Beng",
    "marathi": "mar_Deva",
    "gujarati": "guj_Gujr",
    "punjabi": "pan_Guru",
    "odia": "ory_Orya",
    "assamese": "asm_Beng",
}


def detect_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def get_torch_dtype(device: torch.device):
    if device.type == "cuda":
        return torch.float16
    return torch.float32


class IndicTranslator:
    def __init__(self):
        self.device = detect_device()
        self.dtype = get_torch_dtype(self.device)
        print(f"Using device: {self.device}")
        print(f"Using dtype: {self.dtype}")

        self.ip = IndicProcessor(inference=True)

        self.en_indic_tokenizer = AutoTokenizer.from_pretrained(
            EN_INDIC_MODEL,
            trust_remote_code=True
        )
        self.indic_en_tokenizer = AutoTokenizer.from_pretrained(
            INDIC_EN_MODEL,
            trust_remote_code=True
        )

        self.en_indic_model = self._load_model(EN_INDIC_MODEL)
        self.indic_en_model = self._load_model(INDIC_EN_MODEL)

    def _load_model(self, model_name: str):
        load_kwargs = {
            "trust_remote_code": True,
        }

        if self.device.type == "cuda":
            load_kwargs["torch_dtype"] = torch.float16
        elif self.device.type == "mps":
            load_kwargs["torch_dtype"] = torch.float32
        else:
            load_kwargs["torch_dtype"] = torch.float32

        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            **load_kwargs
        )
        model = model.to(self.device)
        model.eval()
        return model

    def _ensure_list(self, texts: Union[str, List[str]]) -> List[str]:
        if isinstance(texts, str):
            return [texts]
        return texts

    def _translate_batch(
        self,
        texts: Union[str, List[str]],
        src_lang: str,
        tgt_lang: str,
        model,
        tokenizer,
        max_length: int = 256,
        num_beams: int = 5,
    ) -> Union[str, List[str]]:
        text_list = self._ensure_list(texts)

        batch = self.ip.preprocess_batch(
            text_list,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
        )

        inputs = tokenizer(
            batch,
            truncation=True,
            padding="longest",
            return_tensors="pt",
            return_attention_mask=True,
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            generated_tokens = model.generate(
                **inputs,
                use_cache=True,
                min_length=0,
                max_length=max_length,
                num_beams=num_beams,
                num_return_sequences=1,
            )

        decoded = tokenizer.batch_decode(
            generated_tokens,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )

        translations = self.ip.postprocess_batch(decoded, lang=tgt_lang)

        if isinstance(texts, str):
            return translations[0]
        return translations

    def english_to_indic(
        self,
        texts: Union[str, List[str]],
        target_lang_code: str
    ) -> Union[str, List[str]]:
        return self._translate_batch(
            texts=texts,
            src_lang="eng_Latn",
            tgt_lang=target_lang_code,
            model=self.en_indic_model,
            tokenizer=self.en_indic_tokenizer,
        )

    def indic_to_english(
        self,
        texts: Union[str, List[str]],
        source_lang_code: str
    ) -> Union[str, List[str]]:
        return self._translate_batch(
            texts=texts,
            src_lang=source_lang_code,
            tgt_lang="eng_Latn",
            model=self.indic_en_model,
            tokenizer=self.indic_en_tokenizer,
        )

    def english_to_hindi(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "hin_Deva")

    def hindi_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "hin_Deva")

    def english_to_tamil(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "tam_Taml")

    def tamil_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "tam_Taml")

    def english_to_telugu(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "tel_Telu")

    def telugu_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "tel_Telu")

    def english_to_kannada(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "kan_Knda")

    def kannada_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "kan_Knda")

    def english_to_malayalam(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "mal_Mlym")

    def malayalam_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "mal_Mlym")

    def english_to_bengali(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "ben_Beng")

    def bengali_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "ben_Beng")

    def english_to_marathi(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "mar_Deva")

    def marathi_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "mar_Deva")

    def english_to_gujarati(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "guj_Gujr")

    def gujarati_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "guj_Gujr")

    def english_to_punjabi(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "pan_Guru")

    def punjabi_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "pan_Guru")

    def english_to_odia(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "ory_Orya")

    def odia_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "ory_Orya")

    def english_to_assamese(self, texts: Union[str, List[str]]):
        return self.english_to_indic(texts, "asm_Beng")

    def assamese_to_english(self, texts: Union[str, List[str]]):
        return self.indic_to_english(texts, "asm_Beng")

    def english_to_language(self, texts: Union[str, List[str]], language_name: str):
        language_name = language_name.strip().lower()
        if language_name not in LANGUAGE_CODES:
            raise ValueError(f"Unsupported language: {language_name}")
        if language_name == "english":
            return texts
        return self.english_to_indic(texts, LANGUAGE_CODES[language_name])

    def language_to_english(self, texts: Union[str, List[str]], language_name: str):
        language_name = language_name.strip().lower()
        if language_name not in LANGUAGE_CODES:
            raise ValueError(f"Unsupported language: {language_name}")
        if language_name == "english":
            return texts
        return self.indic_to_english(texts, LANGUAGE_CODES[language_name])


if __name__ == "__main__":
    translator = IndicTranslator()

    en_text = [
        "When I was young, I used to go to the park every day.",
        "We watched a new movie last week, which was very inspiring.",
    ]

    hi_text = [
        "जब मैं छोटा था, मैं हर रोज़ पार्क जाता था।",
        "हमने पिछले सप्ताह एक नई फिल्म देखी जो कि बहुत प्रेरणादायक थी।",
    ]

    ta_text = [
        "நான் சிறியவனாக இருந்தபோது, தினமும் பூங்காவிற்கு செல்வேன்.",
        "கடந்த வாரம் நாங்கள் ஒரு புதிய திரைப்படம் பார்த்தோம்.",
    ]

    print("\n--- English to Hindi ---")
    results = translator.english_to_hindi(en_text)
    for src, tgt in zip(en_text, results):
        print("EN:", src)
        print("HI:", tgt)
        print()

    print("\n--- Hindi to English ---")
    results = translator.hindi_to_english(hi_text)
    for src, tgt in zip(hi_text, results):
        print("HI:", src)
        print("EN:", tgt)
        print()

    print("\n--- English to Tamil ---")
    results = translator.english_to_tamil(en_text)
    for src, tgt in zip(en_text, results):
        print("EN:", src)
        print("TA:", tgt)
        print()

    print("\n--- Tamil to English ---")
    results = translator.tamil_to_english(ta_text)
    for src, tgt in zip(ta_text, results):
        print("TA:", src)
        print("EN:", tgt)
        print()

    print("\n--- Generic English to Marathi ---")
    print(translator.english_to_language("India is a beautiful country.", "marathi"))

    print("\n--- Generic Hindi to English ---")
    print(translator.language_to_english("आप कैसे हैं?", "hindi"))
    
