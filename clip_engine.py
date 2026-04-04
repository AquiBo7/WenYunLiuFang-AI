import os
import time
from PIL import Image
from transformers import pipeline

os.environ["TRANSFORMERS_OFFLINE"]="1"
os.environ["HF_HUB_OFFLINE"]="1"

class VisionEngine:
    def __init__(self, model_dir="./modelcache1"):
        print(f"Path assigned to: {model_dir}")
        start_time = time.time()

        try:

            self.classifier = pipeline(
                "zero-shot-image-classification",
                model=model_dir,
                tokenizer=model_dir
            )
            print(f"Engine ready in {time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"Engine stall: {e}")

        self.tags = [
            "山水", "梅花", "楼阁", "长城", "汉服", "水墨画", "古寺", "雪景", "明月",
            "现代跑车", "机甲奥特曼", "电子产品", "高楼大厦", "二次元动漫","美食"
        ]

    def detect_tags(self, img_path):
        try:
            image = Image.open(img_path)
            return self.classifier(image, candidate_labels=self.tags)[:3]
        except Exception as e:
            return None


if __name__ == "__main__":
    engine = VisionEngine()
    res = engine.detect_tags("test.jpg")
    if res:
        print("Top Identifications:")
        for i in res:
            print(f" >> {i['label']}: {i['score']:.4f}")