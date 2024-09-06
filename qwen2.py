import torch
import json
import os

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from data import Data
from fix_busted_json import repair_json

class Qwen2(Data):
    def __init__(self) -> None:
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "mps")
        self.xlsx_path = "matching_dates_cleaned.xlsx"

    def __repr__(self) -> str:
        return "Klasa do obsługi modelu Qwen2"

    def get_model(self):
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            "Qwen/Qwen2-VL-2B-Instruct",
            torch_dtype=torch.bfloat16,
            # attn_implementation="flash_attention_2",
            device_map=self.device,
        )

        return model

    def get_processor(self):
        # min and max pixels for the processor to boost the performance
        min_pixels = 256*28*28
        max_pixels = 1280*28*28
        processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct", min_pixels=min_pixels, max_pixels=max_pixels)

        return processor
    
    def get_images_for_training(self, folder_path: str = None) -> list[str]:
        images_path: list[str] = []

        for root, dirs, files in os.walk(folder_path):
            for file in sorted(files):
                if file.endswith(".png"):
                    images_path.append(os.path.join(root, file))
        
        return images_path

    def get_messages(self) -> list:
        df = self.get_xlsx_data(self.xlsx_path)

        images_path = self.get_images_for_training(folder_path = df["Image folder path"].iloc[0])

        messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": img_path} for img_path in images_path 
                    ] + [
                        {"type": "image", "image": "lemkin-pdf/2014/WDU20140001589/O/D20141589_png/page_0.png"},
                        {"type": "json", "json": df["JSON file path"].iloc[0]},
                        {"type": "text", "text": "Can you make json from last image similar to what I gave you in json type and comparing structure to all another images? As output give me just json structure which can be dumped. Use polish language and letters as well."},
                    ],
                }
            ]

        return messages

    def get_input(self) -> dict:
        processor = self.get_processor()
        text = processor.apply_chat_template(
            self.get_messages(), tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(self.get_messages())
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.device)

        return inputs

    def get_outputs(self) -> list:
        processor = self.get_processor()
        model = self.get_model()
        input = self.get_input()

        generated_ids = model.generate(**input, max_new_tokens=16384)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(input.input_ids, generated_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        
        return output_text
    
    def repair_json(self, json_text: str) -> str:
        return repair_json(json_text)

    def create_json(self) -> json:
        for elem in self.get_outputs():
            cleaned_text = elem.replace("```json\n", "").replace("```", "").strip()

            cleaned_text = " ".join(cleaned_text.split())
            cleaned_text = "".join(cleaned_text.splitlines())

            print("Generated text before loading to JSON:")
            print(cleaned_text)

            try:
                json_obj = json.loads(cleaned_text)
                with open("output.json", "w") as f:
                    json.dump(json_obj, f, indent=4)
                    print("JSON file saved successfully!")
            except json.JSONDecodeError as e:
                print("Error loading JSON:", e)
                with open("error_output.txt", "w") as error_file:
                    error_file.write(cleaned_text)
                print("Błędny JSON zapisany w error_output.txt")

                json_obj = self.repair_json(cleaned_text)
                with open("output_repaired.json", "w") as f:
                    json.dump(json_obj, f, indent=4)
                    print("JSON file saved successfully!")
