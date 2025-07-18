import sqlite3
import uuid
from langgraph.types import   Command
from image_agent.graph import create_image_graph
from .nodes import (
    should_research_node,
    content_generation_agent,
    human_review,
    revise_content_agent,
    check_image,
    final_node
)
from langgraph.graph import StateGraph, END, START
from research_agent.graph import create_research_graph
from .state import SocialMediaState
from langgraph.checkpoint.sqlite import SqliteSaver
import os
from dotenv import load_dotenv
load_dotenv()


def create_social_media_workflow():

    os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Social Media Agent Workflow"
    research_node = create_research_graph()
    image_node = create_image_graph()

    social_media_workflow = StateGraph(SocialMediaState)

    # --- Add nodes ---

    social_media_workflow.add_node("should_research_node", should_research_node)
    social_media_workflow.add_node("research_node", research_node)
    social_media_workflow.add_node("content_generation_agent", content_generation_agent)
    social_media_workflow.add_node("human_review", human_review)
    social_media_workflow.add_node("revise_content_agent", revise_content_agent)
    social_media_workflow.add_node("check_image", check_image)
    social_media_workflow.add_node("image_node", image_node)
    social_media_workflow.add_node("final_node", final_node)
  

    # --- Add start node ---
    social_media_workflow.add_edge(START, "should_research_node")

    # --- After research, go to content generation ---
    social_media_workflow.add_edge("research_node", "content_generation_agent")

    # --- After content generation, go to human review ---
    social_media_workflow.add_edge("content_generation_agent", "human_review")


    # --- After revision, go back to review ---
    social_media_workflow.add_edge("revise_content_agent", "check_image")
    social_media_workflow.add_edge("final_node", END)

   

    # --- After image generation, go to finalize ---
    social_media_workflow.add_edge("image_node", "final_node")
    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)
    return social_media_workflow.compile(checkpointer=memory)


if __name__ == "__main__":
    graph = create_social_media_workflow()
    config = {"configurable": {"thread_id": 1212}}
    messages = [
        {"role": "user", "content": "I want to create a post about the benefits of meditation for mental health."},
    ]
    result = graph.invoke({"messages": messages, 
                           "tone": "engaging", "include_image": False,
                           }, config=config)
    print(result["__interrupt__"])
    final_result = graph.invoke(Command(resume={"approved": False, "comments": "less professional and more friendly"}), config=config)
    print(final_result)
