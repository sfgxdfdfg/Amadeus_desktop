from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_id = ""
save_path = ""  # Local folder

# Download and save model + tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)

tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)
