from flask import Flask, request, render_template, jsonify
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image
import os

app = Flask(__name__)

# Load the model and required components
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Model generation parameters
max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

# Image caption generator
def generator(image_path):
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert(mode="RGB")

    pixel_values = feature_extractor(images=[image], return_tensors='pt').pixel_values.to(device)
    output_ids = model.generate(pixel_values, **gen_kwargs)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

    return caption

# Route for home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"})

        image = request.files["image"]
        if image.filename == "":
            return jsonify({"error": "No selected file"})

        image_path = os.path.join("static", image.filename)
        image.save(image_path)

        caption = generator(image_path)
        return render_template("index.html", image_path=image_path, caption=caption)

    return render_template("index.html", image_path=None, caption=None)

if __name__ == "__main__":
    app.run(debug=True)
