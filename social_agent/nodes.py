import random
from langgraph.types import  interrupt, Command
from typing import Literal
from .state import SocialMediaState, ShouldResearch
from .prompts  import content_generation_prompt, revise_content_prompt, should_research_prompt
from load_model import load_model
from langgraph.graph import END

llm = load_model("gemini-2.0-flash")


def should_research_node(state: SocialMediaState) -> Command[Literal["research_node", "content_generation_agent"]]:
    """
    Uses the LLM to decide if the content requires additional research.

    Returns:
        str: "research_node" if research is needed, otherwise "content_generation_agent"
    """
    user_message = state["messages"][-1].content
    prompt = should_research_prompt(user_message)

    response = llm.with_structured_output(ShouldResearch).invoke(prompt)
    print(f"LLM response: {response} user_message: {user_message}")
    answer = response["should_research"]

    return Command(
        goto="research_node" if answer else "content_generation_agent",
        update={"should_research": answer,})


def content_generation_agent(state: SocialMediaState) -> SocialMediaState:
    print("📝 Generating content...")

    user_message = state["messages"][-1]
    research_content = state.get("content", "")
    platform = state.get("platform", "facebook")

    prompt = content_generation_prompt(user_message, research_content, platform)
    response = llm.invoke(prompt)
    state["posts"] = response.content
    return state


def check_image(state: SocialMediaState) -> Command[Literal["image_node", "final_node"]]:
    print("🖼️ Deciding whether to generate image...")
    return Command(goto="image_node") if state.get("include_image") else Command(goto="final_node")



def human_review(state: SocialMediaState) ->  Command[Literal["check_image", "revise_content_agent"]]:
    print("🧑‍💻 Human reviewing post...")

    answer = interrupt({"query": 'check the ideas below and choose the one you want',
                          'ideas': state.get('posts', ''),})
    
    print(f"Human review answer: {answer} ..................")


    if answer["approved"]:
        return Command(goto="check_image", update={"approved": answer["approved"]})
        
    else:
        return Command(goto="revise_content_agent", update={"approved": answer["approved"], "feedback": answer["comments"]})
        


def revise_content_agent(state: SocialMediaState) -> SocialMediaState:
    print("🔁 Revising content... \n\n\n\n")

    human_message = state["messages"][0].content
    original_content = state.get("posts", "")
    feedback = state.get("feedback", "")

    prompt = revise_content_prompt(human_message, original_content, feedback)
    response = llm.invoke(prompt)
    state["ideas"] = response.content 
    state["feedback"] = None
    return state

def final_node(state: SocialMediaState) -> SocialMediaState:
    print("✅ Finalizing post...")
    return {"posts": state["posts"]}



# --- WORKFLOW SETUP ---