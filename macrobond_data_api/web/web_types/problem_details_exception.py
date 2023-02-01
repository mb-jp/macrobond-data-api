from typing import Optional, Dict, Any, List, TYPE_CHECKING


if TYPE_CHECKING:  # pragma: no cover
    from requests import Response  # type: ignore


class ProblemDetailsException(Exception):
    """
    A machine-readable format for specifying errors in HTTP API responses based on
    https://tools.ietf.org/html/rfc7807.
    """

    response: "Response"

    type: Optional[str]
    title: Optional[str]
    status: Optional[int]
    detail: Optional[str]
    instance: Optional[str]
    extensions: Optional[Dict[str, Optional[Any]]]

    def __init__(
        self,
        response: "Response",
        _type: str = None,
        title: str = None,
        status: int = None,
        detail: str = None,
        instance: str = None,
        extensions: Dict[str, Optional[Any]] = None,
        errors: Dict[str, List[str]] = None,
    ) -> None:
        request = response.request
        super().__init__(
            (
                f"http {request.method} request to {request.path_url}\n"
                f"response.status_code: {str(response.status_code)}\n"
                f"type: {str(_type)}\n"
                f"title: {str(title)}\n"
                f"status: {str(status)}\n"
                f"detail: {str(detail)}\n"
                f"instance: {str(instance)}\n"
                f"extensions: {str(extensions)}\n"
                f"errors: {str(errors)}\n"
            )
        )

        self.response = response

        self.type = _type
        """
            A URI reference [RFC3986] that identifies the problem type. This specification
            encourages that, when dereferenced, it provide human-readable documentation for
            the problem type (e.g., using HTML [W3C.REC-html5-20141028]). When this member
            is not present, its value is assumed to be "about:blank".
        """

        self.title = title
        """
            A short, human-readable summary of the problem type.It SHOULD NOT change from
            occurrence to occurrence of the problem, except for purposes of localization(e.g.,
            using proactive content negotiation; see[RFC7231], Section 3.4).
        """

        self.status = status
        """
            The HTTP status code([RFC7231], Section 6) generated by the origin server for
            this occurrence of the problem.
        """

        self.detail = detail
        """
            A human-readable explanation specific to this occurrence of the problem.
        """

        self.instance = instance
        """
            A URI reference that identifies the specific occurrence of the problem.It may
            or may not yield further information if dereferenced.
        """

        self.extensions = extensions
        """
            Summary:
            Gets the Optional[Dict[str, Optional[Any]]] for extension members.
            Problem type definitions MAY extend the problem details object with additional
            members. Extension members appear in the same namespace as other members of a
            problem type.

            Remarks:
            The round-tripping behavior for Microsoft.AspNetCore.Mvc.ProblemDetails.Extensions
            is determined by the implementation of the Input \\ Output formatters. In particular, 
            complex types or collection types may not round-trip to the original type when
            using the built-in JSON or XML formatters.
        """

        self.errors = errors
        """
            Gets the validation errors associated with this instance
        """

    @classmethod
    def create_from_response(cls, response: "Response") -> "ProblemDetailsException":
        json = response.json()

        _type = json.get("type")
        title = json.get("title")
        status = json.get("status")
        detail = json.get("detail")
        instance = json.get("instance")
        extensions = json.get("extensions")
        errors = json.get("errors")

        return ProblemDetailsException(
            response, _type, title, status, detail, instance, extensions, errors
        )
