"""
MIT License

Copyright (c) 2020 akrocynova

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from papermc import __version__
import logging
import requests
import os

class APIError(Exception):
    pass

class ProjectNotFoundError(Exception):
    pass

class BaseAPIv1:
    def __init__(self, base_url: str = "https://papermc.io/api/v1", project_name: str = None) -> None:
        """Base API v1 class"""

        self.logger = logging.getLogger("papermc")
        self._base_url = base_url
        self.project_name = project_name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _get(self, request: str, method: str = "GET",) -> requests.Response:
        """Send an HTTP request to the Paper API"""

        if self.project_name == None:
            raise NotImplementedError("BaseAPIv1 cannot be used without a project name")

        req_url = "{}/{}{}".format(
            self._base_url,
            self.project_name,
            request
        )

        self.logger.debug("{} {}".format(method, req_url))
        response = requests.request(
            method,
            req_url,
            headers={
                "User-Agent": "python-papermc-{}".format(__version__)
            }
        )

        if response.status_code != 200:
            try:
                error = response.json().get("error", dict())

            except:
                response.raise_for_status()

            raise APIError("HTTP {}: {}".format(
                error.get("code", response.status_code),
                error.get("message", "Undefined")
            ))

        return response

    def get_versions(self) -> list:
        """Get a list of supported Minecraft versions"""

        return self._get("").json().get("versions", list())

    def get_latest_version(self) -> str:
        """Get the latest supported Minecraft version"""

        return self.get_versions()[0]

    def get_builds(self, version: str) -> list:
        """Get a list of builds for a specific version"""

        return self._get("/{}".format(version)).json().get("builds", dict()).get("all", list())

    def get_latest_build(self, version: str) -> str:
        """Get the latest build for a specific version"""

        return self._get("/{}/latest".format(version)).json().get("build", "")

    def download_build(self, version: str, build: str) -> bytes:
        """Download the JAR file and return its bytes
        `version` and `build` can both be `latest`"""

        if version == "latest":
            version = self.get_latest_version()

        response = self._get(
            "/{}/{}/download".format(
                version,
                build
            )
        )

        if response.headers.get("content-type") != "application/java-archive":
            raise APIError("Expected Content-Type 'application/java-archive', got '{}'".format(
                response.headers.get("content-type")
            ))

        return response.content

    def download_build_to_file(self, filepath: str, version: str, build: str) -> None:
        """Download the JAR file and save it to the given path
        `version` and `build` can both be `latest`"""

        with open(filepath, "wb") as outfile:
            outfile.write(self.download_build(version, build=build))
            outfile.flush()

class Paper(BaseAPIv1):
    def __init__(self):
        super().__init__(project_name="paper")

class Waterfall(BaseAPIv1):
    def __init__(self):
        super().__init__(project_name="waterfall")

class Travertine(BaseAPIv1):
    def __init__(self):
        super().__init__(project_name="travertine")

def get_from_name(project_name: str) -> BaseAPIv1:
    """Return an API object from the project name"""

    if project_name == "paper":
        return Paper()
    elif project_name == "waterfall":
        return Waterfall()
    elif project_name == "travertine":
        return Travertine()
    else:
        raise ProjectNotFoundError(project_name)