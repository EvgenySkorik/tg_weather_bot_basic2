import requests


def _make_response(method: str, url: str, headers: Dict, params: Dict,
                   timeout: int, success=200):
    res = requests.request(
        method,
        url,
        headers=headers,
        params=params,
        timeout=timeout,
    )

    status_code = res.status_code

    if status_code == success:
        return res

    return status_code

