import torch
import json

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from data import Data

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

    def get_messages(self) -> list:
        df = self.get_xlsx_data(self.xlsx_path)
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_0.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_1.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_2.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_3.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_4.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_5.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_6.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_7.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_8.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_9.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_10.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_11.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_12.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_13.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_14.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_15.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_16.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_17.png",
                        "image": "lemkin-pdf/2014/WDU20140001826/T/D20141826TK_png/page_18.png",
                        "image": "lemkin-pdf/2014/WDU20140001589/O/D20141589_png/page_0.png"
                    },
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

        generated_ids = model.generate(**input, max_new_tokens=4096)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(input.input_ids, generated_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        
        return output_text

    def create_json(self) -> json:
        for elem in self.get_outputs():
            cleaned_text = elem.replace("```json\n", "").replace("```", "").strip()

            # usuwanie nadmiarowych spacji i znaków nowej linii
            cleaned_text = " ".join(cleaned_text.split())
            cleaned_text = "".join(cleaned_text.splitlines())

            print(cleaned_text)

            # save the output to a JSON file
            try:
                with open("output.json", "w") as f:
                    json_obj = json.loads(cleaned_text)
                    json.dump(json_obj, f, indent=4)
                    print("JSON file saved successfully!")
            except Exception as e:
                print("Error saving JSON file:", e)
                pass