import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from modules.data_handlers.executable_file_redirector import *

class EmotionAnalysis:
    def __init__(self) -> None:
        self.model_path = os.path.join("emotion_analysis", "custom_models", "amadeus_1")
        self.model_path_exe_compatible = convert().get_resource_path(self.model_path)

        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path_exe_compatible)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path_exe_compatible)

        self.emotion_pipeline = pipeline(
            task="text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            top_k=1
        )

    
    def analyze_emotion(self, sentence: str) -> str:
        results = self.emotion_pipeline(sentence)[0]
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        top_result = sorted_results[0]["label"]

        ''' 
        for r in sorted_results[:5]:
            print(f"{r['label']}: {r['score']:.3f}")
        '''
        
        return top_result