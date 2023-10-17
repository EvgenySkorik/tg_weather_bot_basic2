import requests
import json


def far_to_cel(num: float) -> float:
    """Функция конвертации фаренгейт в цельсии"""
    return round((num - 32) / 1.8, 2)


def _get_response(url: str, usr_city: str, headers):
    response = requests.get(url + usr_city, headers=headers)
    status_code = response.status_code
    if status_code == 200:
        data = json.loads(response.text)
        return far_to_cel(data.get('main', None).get('temp', None)), \
            far_to_cel(data.get('main', None).get('feels_like', None)), \
            far_to_cel(data.get('main', None).get('temp_min', None)), \
            far_to_cel(data.get('main', None).get('temp_max', None))


# def _get_response_5days(url: str, usr_city, headers):
#     response = requests.get(url + usr_city, headers=headers)
#     status_code = response.status_code
#     if status_code == 200:
#         data = json.loads(response.text)
#         coord_lon, coord_lat = data.get('coord', None).get('lon', None), data.get('coord', None).get('lat', None)
#
#         response_5days = requests.get(url + 'fivedaysforcast/' + coord_lon + '/' + coord_lat)
#         data_5days = json.loads(response_5days.text)
#         return far_to_cel(data.get('main', None).get('temp', None)), \
#             far_to_cel(data.get('main', None).get('feels_like', None))


class SiteApiInterface():

    @staticmethod
    def get_response():
        return _get_response


if __name__=='main':
    _get_response()
    SiteApiInterface()