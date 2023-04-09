""" Файл для функции получения детальной информации об отеле по его id. """

from hotel_API.basic_request import api_request
from loguru import logger


@logger.catch()
def detail_info(hotel_id: str | int) -> dict:
    """ Функция получения от API отелей детальной информации об отеле. """
    
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": str(hotel_id)
    }
    
    response = api_request("properties/v2/detail", payload, "POST")
    result_dict = raw_detail_hotel_info_handle(response)
    return result_dict


@logger.catch()
def raw_detail_hotel_info_handle(raw_hotel_info: dict) -> dict:
    """ Функция обработки сырого ответа от API с детальной информацией об отеле
        и сохранение в словарь только нужной информации. """
    
    result = dict()
    
    data = raw_hotel_info["data"]
    property_info = data["propertyInfo"]
    summary = property_info["summary"]
    result["name"] = summary["name"]
    result["tagline"] = summary["tagline"]
    result["address"] = summary["location"]["address"]["addressLine"]
    
    images = list()
    for i_image in property_info["propertyGallery"]["images"]:
        i_image_url = i_image["image"]["url"]
        images.append(i_image_url)
    result["images"] = images
    
    result["score"] = property_info["reviewInfo"]["summary"]["overallScoreWithDescriptionA11y"]["value"]

    logger.debug(result)
    return result
