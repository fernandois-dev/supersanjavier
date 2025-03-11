import re

import repath


class TemplateRoute:
    def __init__(self, route: str, params: dict = None) -> None:
        self.__last_params = {}
        self.route = route.split('?')[0]
        self.params = self.set_params(params, route)  # Call set_params with self.route


    def set_params(self, params: dict, route: str) -> dict:
        """Combines provided parameters with URL query parameters."""
        combined_params = {}
        if params:
            combined_params.update(params)  # Add provided parameters

        try:
            query_params = route.split('?')[1]
            url_params = {k: v for k, v in [p.split('=') for p in query_params.split('&')]}
            combined_params.update(url_params)  # Add URL query parameters
        except IndexError:
            pass  # No query parameters in the URL

        #Handle missing origin parameter:
        if "origin" not in combined_params and self.route:
            split = self.route.split("/")
            combined_params["origin"] = split[len(split) - 2]
        return combined_params


    def get_params(self) -> dict:
        """Returns all parameters as a single dictionary."""
        return self.params

    def match(self, route_template: str) -> bool:
        # remove old properties
        for k in self.__last_params:
            setattr(self, k, None)

        # perform new match
        pattern = repath.pattern(route_template)
        match = re.match(pattern, self.route)

        if match:
            self.__last_params = match.groupdict()
            for k, v in self.__last_params.items():
                setattr(self, k, v)
            return True
        return False