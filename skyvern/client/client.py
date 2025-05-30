# This file was auto-generated by Fern from our API Definition.

import typing
from .environment import SkyvernEnvironment
import httpx
from .core.client_wrapper import SyncClientWrapper
# Temporarily disable client imports to get application running
# TODO: Fix client module structure
print("WARNING: Client imports disabled temporarily to resolve module issues")

# Create dummy client classes to prevent AttributeError
class DummyClient:
    def __init__(self, client_wrapper=None):
        self.client_wrapper = client_wrapper

AgentClient = DummyClient
AsyncAgentClient = DummyClient
WorkflowsClient = DummyClient
AsyncWorkflowsClient = DummyClient
ArtifactsClient = DummyClient
AsyncArtifactsClient = DummyClient
BrowserSessionClient = DummyClient
AsyncBrowserSessionClient = DummyClient
CredentialsClient = DummyClient
AsyncCredentialsClient = DummyClient
from .core.client_wrapper import AsyncClientWrapper


class Skyvern:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : SkyvernEnvironment
        The environment to use for requests from the client. from .environment import SkyvernEnvironment



        Defaults to SkyvernEnvironment.PRODUCTION



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from skyvern import Skyvern

    client = Skyvern(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: SkyvernEnvironment = SkyvernEnvironment.PRODUCTION,
        api_key: typing.Optional[str] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.agent = AgentClient(client_wrapper=self._client_wrapper)
        self.workflows = WorkflowsClient(client_wrapper=self._client_wrapper)
        self.artifacts = ArtifactsClient(client_wrapper=self._client_wrapper)
        self.browser_session = BrowserSessionClient(client_wrapper=self._client_wrapper)
        self.credentials = CredentialsClient(client_wrapper=self._client_wrapper)


class AsyncSkyvern:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : SkyvernEnvironment
        The environment to use for requests from the client. from .environment import SkyvernEnvironment



        Defaults to SkyvernEnvironment.PRODUCTION



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from skyvern import AsyncSkyvern

    client = AsyncSkyvern(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: SkyvernEnvironment = SkyvernEnvironment.PRODUCTION,
        api_key: typing.Optional[str] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.agent = AsyncAgentClient(client_wrapper=self._client_wrapper)
        self.workflows = AsyncWorkflowsClient(client_wrapper=self._client_wrapper)
        self.artifacts = AsyncArtifactsClient(client_wrapper=self._client_wrapper)
        self.browser_session = AsyncBrowserSessionClient(client_wrapper=self._client_wrapper)
        self.credentials = AsyncCredentialsClient(client_wrapper=self._client_wrapper)


def _get_base_url(*, base_url: typing.Optional[str] = None, environment: SkyvernEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
