from django.utils.deprecation import MiddlewareMixin

import logging


logger = logging.getLogger(__name__)


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        logger.info(request.body)
        if request.headers.get("Authorization"):
            logger.info(request.headers.get("Authorization"))
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_response(self, request, response):
        logger.info(response.content)
        return response
