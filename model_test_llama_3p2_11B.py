# tested with Python 3.12.7

import requests
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor
import time

model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(model_id)

url = input("IMAGE URL:")
image = Image.open(requests.get(url, stream=True).raw)
start_time = time.time()
messages = [
    {"role": "user", "content": [
        {"type": "image"},
        {"type": "text", "text": "Görseldeki faturada bulunan elektrik faturası miktarı ne kadardır?"}
    ]}
]
input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(
    image,
    input_text,
    add_special_tokens=False,
    return_tensors="pt"
).to(model.device)

output = model.generate(**inputs, max_new_tokens=30)
print(processor.decode(output[0]))
print("--- %s seconds ---" % (time.time() - start_time))