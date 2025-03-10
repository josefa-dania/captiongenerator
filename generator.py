from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "image" not in request.files:
            return redirect(url_for("home"))

        image = request.files["image"]
        if image.filename == "":
            return redirect(url_for("home"))

        image_path = os.path.join("static", image.filename)
        image.save(image_path)

        # Example caption generation (replace with your generator logic)
        caption = "Sample caption for uploaded image"

        return redirect(url_for("result", image_path=image_path, caption=caption))

    return render_template("index.html", image_path=None, caption=None)

@app.route("/result")
def result():
    image_path = request.args.get("image_path")
    caption = request.args.get("caption")
    return render_template("index.html", image_path=image_path, caption=caption)

if __name__ == "__main__":
    app.run(debug=True)

