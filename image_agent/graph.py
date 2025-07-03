from .state import ImageGenState
from .nodes import image_instruction_node, generate_image
from langgraph.graph import StateGraph

def create_image_graph() -> StateGraph:
    """
    Creates and compiles a LangGraph state graph for the image generation workflow.

    This graph consists of two main nodes:
    1. 'image_instruction': Generates a detailed visual description based on the user's message and platform context.
    2. 'generate_image': Uses the generated description to produce a base64-encoded image.

    Workflow:
        Entry point -> 'image_instruction' → 'generate_image'

    Returns:
        StateGraph: A compiled LangGraph graph representing the image generation workflow.
    """
    image_workflow = StateGraph(ImageGenState)

    image_workflow.add_node("image_instruction", image_instruction_node)
    image_workflow.add_node("generate_image", generate_image)

    image_workflow.set_entry_point("image_instruction")
    image_workflow.add_edge("image_instruction", "generate_image")

    image_graph = image_workflow.compile()
    return image_graph
