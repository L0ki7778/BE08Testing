from rest_framework.throttling import UserRateThrottle #type: ignore
from rest_framework.request import Request #type: ignore
from rest_framework.views import APIView #type: ignore


# class QuestionThrottle(UserRateThrottle):
#     scope = 'question'
    
#     def allow_request(self, request:Request, view:APIView):
#         scope = 'question-' + request.method.lower()
#         if scope in self.THROTTLE_RATES: #type: ignore
#             self.scope = scope
#             self.rate = self.get_rate()
#             self.num_requests, self.duration = self.parse_rate(self.rate) #type: ignore
        
#         return super().allow_request(request, view) #type:ignore

class QuestionGetThrottle(UserRateThrottle):
    scope = 'question-get'
    

class QuestionPostThrottle(UserRateThrottle):
    scope = 'question-post'
    