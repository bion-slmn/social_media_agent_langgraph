from langgraph.graph import  MessagesState

class ImageGenState(MessagesState):
    image_url: str
    image_instruction: str
    platform: str