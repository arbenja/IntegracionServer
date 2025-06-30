from simple_history.middleware import HistoricalRecords

class HistoryRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from simple_history.utils import update_change_reason
        HistoricalRecords.thread.request = request
        return self.get_response(request)
