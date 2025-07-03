from load_model import load_model
from .state import ImageGenState
import logging

# Load models
image_llm = load_model("models/gemini-2.0-flash-exp-image-generation")
llm = load_model("gemini-2.0-flash")


def image_instruction_node(state: ImageGenState) -> ImageGenState:
    """
    Generates a detailed image description based on the latest user message and platform context.
    This description will guide the image generation model.
    """
    user_message = state.get("messages", [])[-1] if state.get("messages") else ""
    platform = state.get("platform", "Facebook")

    print("📝 Generating image instruction...")

    if not user_message:
        logging.warning("No user message found in state.")
        state["image_instruction"] = ""
        return state

    prompt = (
        f"A user is writing a social media post for {platform} with the following message:\n\n"
        f"\"{user_message}\"\n\n"
        "Based on this message and platform, describe a visually engaging image that should be created. "
        "Include specific elements like setting, style, mood, and any key objects or people that should appear."
    )

    try:
        response = llm.invoke(prompt)
        state["image_instruction"] = response.content
    except Exception as e:
        logging.error(f"Failed to get image instruction: {e}")
        state["image_instruction"] = ""

    return state


def generate_image(state: ImageGenState) -> ImageGenState:
    """
    Sends the image instruction to the image generation model (Gemini) and stores the base64 image.
    """
    print("🎨 Generating image...")
    image_instruction = state.get("image_instruction", "")

    if not image_instruction:
        logging.warning("No image instruction provided.")
        state["image_url"] = None
        return state

    try:
        response = image_llm.invoke(
            image_instruction,
            generation_config={"response_modalities": ["TEXT", "IMAGE"]}
        )
    except Exception as e:
        logging.error(f"Image generation failed: {e}")
        state["image_url"] = None
        return state

    # Extract base64 image string
    content = response.content
    image_data = extract_image_data(content)

    if not image_data:
        logging.warning("No image data found in Gemini response.")

    state["image_url"] = image_data
    return state


def extract_image_data(content) -> str:
    """
    Extracts base64 image data from Gemini response content.
    """
    for item in content:
        if isinstance(item, dict):
            if "inline_data" in item:
                return item["inline_data"].get("data")
            elif "image_url" in item and "url" in item["image_url"]:
                
                data_url = item["image_url"]["url"]
                if data_url.startswith("data:image"):
                    image_data = data_url.split(",")[1]
                    return image_data
    return None
