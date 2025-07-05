# services/social_media_service.py
import uuid
from langgraph.types import Command
from social_agent.graph import create_social_media_workflow

class SocialMediaAgentService:
    def __init__(self):
        self.graph = create_social_media_workflow()

    def stream_message(self, message, include_image=False):
        if not message:
            raise ValueError("Message is required.")

        messages = [{"role": "user", "content": message}]
        thread_id = uuid.uuid4().hex
        config = {"configurable": {"thread_id": thread_id}}

        inputs = {
            "messages": messages,
            "tone": "engaging",
            "include_image": include_image,
        }

        def event_stream():
            try:
                for output in self.graph.stream(inputs, config=config):
                    if "should_research_node" in output:
                        yield f"data: Researching the ideas : {output['should_research_node']}...\n\n"
                    elif "research_node" in output:
                        yield "data: Finished Researching ..............:...\n\n"
                    elif "content_generation_agent" in output:
                        yield "data: Generating posts...\n\n"
                    elif output.get('__interrupt__'):
                        human_review = output['__interrupt__'][0].value
                        yield f"{human_review['ideas']}\n\n"
                    elif output.get('include_image') and output.get('approved'):
                        yield "data: Generating image\n\n"
                    else:
                        yield f"data: {output}\n\n"
            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"

        return event_stream(), thread_id

    def resume_workflow(self, thread_id, approved=True, comments=None):
        if not thread_id:
            raise ValueError("thread_id is required.")

        config = {"configurable": {"thread_id": thread_id}}

        print(f"Resuming workflow... approved: {approved}, comments: {comments}")

        command = Command(resume={"approved": approved})
        if not approved and comments:
            command = Command(resume={"approved": False, "comments": comments})
        

        def event_stream():
            try:
                result = self.graph.stream(command, config=config)
                for output in result:
                    if output.get("revise_content_agent"):
                        yield f"data: Revising the post based on feedback: {comments}\n\n"
                    elif output.get('include_image') :
                        yield "data: Generating image\n\n"
                    elif output.get('final_node'):
                        yield f"{output.get('final_node').get('posts')}\n\n"
                yield "data: [Thread Complete]\n\n"
            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"

        return event_stream()


