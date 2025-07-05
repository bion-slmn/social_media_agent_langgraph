from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from social_agent.graph import create_social_media_workflow
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
from langgraph.types import   Command


@api_view(['GET'])
def status(request):
    return Response({"status": "Social Media Agent is running 🚀"})


class SocialMediaAgentView(APIView):

    def __init__(self, **kwargs):
        self.graph = create_social_media_workflow()

    def post(self, request):
        try:
            include_image = request.data.get("include_image", False)
            message = request.data.get("message")

            if not message:
                return Response({"error": "Message is required."}, status=400)

            messages = [{"role": "user", "content": message}]
            thread_id = uuid.uuid4().hex  # Generate a unique thread ID

            config = {"configurable": {"thread_id": thread_id}}

            result = self.graph.invoke({
                "messages": messages,
                "tone": "engaging",
                "include_image": include_image,
            }, config=config)
            interrupts = result.get("__interrupt__", [])


            return Response({
                "human_review": interrupts[0].value ,
                "thread_id": thread_id,
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def put(self, request):
        
        thread_id = request.data.get("thread_id")
        approved = request.data.get("approved", True)
        print(f"Thread ID: {thread_id}, Approved: {approved}")
        if not thread_id:
            return Response({"error": "thread_id is required."}, status=400)

        config = {"configurable": {"thread_id": thread_id}}

        final_result = self.graph.invoke(
            Command(resume={"approved": True}),
            config=config
        )

        return Response({"result": final_result})


