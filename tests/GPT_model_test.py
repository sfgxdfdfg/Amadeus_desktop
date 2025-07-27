from transformers import GPT2LMHeadModel, AutoTokenizer
import torch

# Load model & tokenizer
model_path = ".\GPT_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Set pad token
tokenizer.pad_token = tokenizer.eos_token

while True:
    # Get user input
    input_text = input("\nEnter your prompt (or 'quit' to exit): ")
    if input_text.lower() == 'quit':
        break
        
    try:
        # Tokenize input (returns dict with input_ids and attention_mask)
        inputs = tokenizer(input_text, return_tensors="pt")
        
        # Generate text
        output = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            pad_token_id=tokenizer.pad_token_id,
            max_length=100,
            temperature=0.7,
            do_sample=True,
        )
        
        # Decode and print
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        print("\nGenerated response:", generated_text)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Tip: Make sure your input is properly formatted text")