import re
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

import logging

from chatttty import settings


class MappingCacheMiddleware(MiddlewareMixin):
    logger = logging.getLogger("chat.middleware.MappingCacheMiddleware")
    cache_map = getattr(settings, "CACHE_MAP", {})

    def get_cache_key(self, request, path):
        user_key = (
            request.user.id
            if request.user.is_authenticated
            else request.session.session_key
        )
        return f"cache_{path}_{user_key}"

    def get_settings(self, path):
        for key_pattern, settings in self.cache_map.items():
            if re.match(key_pattern, path):
                return settings

    @staticmethod
    def replace_with_cookies(pattern, cookies):
        group_names = re.findall(r"\?P<([^>]+)>", pattern)
        url = pattern
        for group in group_names:
            value = cookies.get(group, f"{{{group}}}")
            url = url.replace(f"(?P<{group}>[A-Za-z0-9\\-\\_]+)", value)
        url = re.sub(r"[\\\^\$]", "", url)
        return url

    def process_request(self, request):
        if (settings := self.get_settings(request.path)) and settings.get("method", request.method) == request.method:
            cache_key = self.get_cache_key(request, request.path)
            if cache_value := cache.get(cache_key):
                return cache_value
        for key_path, settings in self.cache_map.items():
            for p in settings["invalidate_ons"]:
                if re.match(p["url"], request.path) and p.get("method", request.method) == request.method:
                    path = self.replace_with_cookies(key_path, request.COOKIES)
                    cache_key = self.get_cache_key(request, path)
                    cache.delete(cache_key)
                    return

    def process_response(self, request, response):
        if (settings := self.get_settings(request.path)) and settings.get("method", request.method) == request.method:
            cache_key = self.get_cache_key(request, request.path)
            if not cache.has_key(cache_key):
                cache.set(cache_key, response, settings.get("cache_time", 60 * 15))
        return response
