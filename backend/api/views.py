from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from social_agent.graph import create_social_media_workflow
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
from langgraph.types import   Command
from .service import SocialMediaAgentService

@api_view(['GET'])
def status(request):
    return Response({"status": "Social Media Agent is running 🚀"})





@api_view(['GET'])
def status(request):
    return Response({"status": "Social Media Agent is running 🚀"})


class SocialMediaAgentView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = SocialMediaAgentService()

    def post(self, request):
        try:
            message = request.data.get("message")
            include_image = request.data.get("include_image", False)


            event_stream, thread_id = self.service.stream_message(message, include_image)
            print(f"Generated thread_id: {thread_id}")
            response = StreamingHttpResponse(event_stream, content_type='text/event-stream')
            response['X-Thread-ID'] = str(thread_id) # Add a custom header
            return response

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=400)

    def put(self, request):
        try:
            thread_id = request.data.get("thread_id")
            comments = request.data.get("comments")
            approved = request.data.get("approved", True)
            print(f"Resuming workflow for thread_id: {thread_id} with approved: {approved}")
            if not thread_id:
                return Response({"error": "thread_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            

            event_stream = self.service.resume_workflow(thread_id, approved, comments)

            return StreamingHttpResponse(event_stream, content_type='text/event-stream')

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
   


