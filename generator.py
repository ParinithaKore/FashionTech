import torch
from diffusers import StableDiffusionPipeline
from rembg import remove
from PIL import Image
import os

app = Flask(_name_, static_folder="static")
CORS(app)

# Load the Stable Diffusion model
model_id = "dreamlike-art/dreamlike-diffusion-1.0"


pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
pipe.to("cpu")  # Use "cuda" if GPU is available

def enhance_prompt(user_prompt):
    blacklist = ["model", "person", "mannequin", "human", "face", "people", "man"]
    for word in blacklist:
        user_prompt = user_prompt.replace(word, "")
    
    suffix = (
    ", single clothing item only, standalone clothing, apparel only, centered, isolated clothing design, "
    "flat lay, product photo, white background, no mannequin, no human, no model, no body parts, front view"
)

    return user_prompt.strip() + suffix


@app.route('/generate', methods=['POST'])
def generate_design():
    data = request.json
    user_prompt = data.get("prompt")
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Enhance the prompt
    prompt = enhance_prompt(user_prompt)

    # Generate the image
    image = pipe(
    prompt,
    negative_prompt = "mannequin, human, model, person, face, body, people, head, full body, arms, legs, background, room, scene, shadows, complex background",
    num_inference_steps=25,
    guidance_scale=7.5
    ).images[0]



    image = image.resize((768, 1024), Image.LANCZOS)
    image_path = os.path.join(app.static_folder, "fashion_design.png")
    image.save(image_path)

    # Remove the background using rembg
    try:
        with Image.open(image_path) as input_image:
            output_image = remove(input_image)
            output_image.save(image_path)  # Overwrite the original with transparent one
    except Exception as e:
        print("❌ Background removal failed:", e)

    return jsonify({
        "message": "Image generated with background removed successfully",
        "image_url": "/static/fashion_design.png"
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if _name_ == "_main_":
    os.makedirs(app.static_folder, exist_ok=True)
    app.run(debug=True)
