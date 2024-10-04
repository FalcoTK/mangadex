from ..error import JSONError, NotFoundError, ConnectionError, FetchErrorr
from curl_cffi.requests import Session
import logging


class manga:
    """
    # COPPYRIGHT MANGA, PROVIDER `MANGADEX <https://mangadex.org/>`_
    Manga reader for fetching manga chapters and their images from MangaDex.

    This class provides methods to fetch chapter details and images using the MangaDex API.
    It includes error handling for connection issues and JSON parsing errors.
    """

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    async def FetchChapterIMG(self, ChapterID: str):
        """
        ### COPPYRIGHT MANGA, PROVIDER `MANGADEX <https://mangadex.org/>`_
        Fetches images for a given chapter ID.

        Args:
            ChapterID (str): The ID of the chapter to fetch images for.

        Returns:
            List[str]: A list of image URLs for the specified chapter.

        Raises:
            ConnectionError: If the response status code is not 200.
            JSONError: If the JSON payload cannot be parsed.
            FetchErrorr: For other general errors during the fetch process.

        Example:

        ```python
            images = await manga_instance.FetchChapterIMG("chapter_id_here")
        """
        with Session(impersonate="chrome120") as s:
            try:
                logging.info(f"Fetching images for chapter ID: {ChapterID}")
                response = s.get(f"https://api.mangadex.org/at-home/server/{ChapterID}")

                if response.status_code != 200:
                    logging.error(
                        f"Failed to fetch Manga Payload. Status code: {response.status_code}"
                    )
                    raise ConnectionError(
                        f"Failed to fetch Manga Payload. Status code: {response.status_code}"
                    )

                try:
                    data = response.json()  # Correctly parse the response as JSON
                    BaseUrl = data.get("baseUrl", "")
                    CHHash = data.get("chapter", {}).get("hash", "")
                    CHData = data.get("chapter", {}).get("data", [])
                    ImageUrl = [f"{BaseUrl}/data/{CHHash}/{image}" for image in CHData]

                    logging.info(
                        f"Successfully fetched images for chapter ID: {ChapterID}"
                    )
                    return ImageUrl
                except ValueError as json_error:
                    logging.error("Failed to parse Manga Payload as JSON.")
                    raise JSONError("Failed to parse Manga Payload.") from json_error
            except Exception as e:
                logging.error(f"An error occurred while fetching Manga Payload: {e}")
                raise FetchErrorr(
                    f"An error occurred while fetching Manga Payload: {e}"
                )

    async def FetchChapter(self, mangaID: str, MaxChapters: int = None):
        """
        ### COPPYRIGHT MANGA, PROVIDER `MANGADEX <https://mangadex.org/>`_
        Fetches chapter details for a given manga ID.

        Args:
            mangaID (str): The ID of the manga to fetch chapters for.
            MaxChapters (int, optional): The maximum number of chapters to fetch. Defaults to 40.
                If the fetch fails, consider decreasing MaxChapters.

        Returns:
                List[Dict[str, Any]]: A list of dictionaries containing chapter details.

        Raises:
            ConnectionError: If the response status code is not 200.
            JSONError: If the JSON payload cannot be parsed.
            FetchErrorr: For other general errors during the fetch process.

        Example:
        ```python
            chapters = await manga_instance.FetchChapter("manga_id_here", MaxChapters=10)
        """
        with Session(impersonate="chrome120") as s:
            try:
                if MaxChapters is None:
                    MaxChapters = 40
                logging.info(
                    f"Fetching chapters for manga ID: {mangaID} with a limit of {MaxChapters} chapters."
                )

                response = s.get(
                    f"https://api.mangadex.org/manga/{mangaID}/feed?limit={MaxChapters}&includes[]=scanlation_group&includes[]=user&order[volume]=desc&order[chapter]=desc&offset=0&contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&contentRating[]=pornographic"
                )

                if response.status_code != 200:
                    logging.error(
                        f"Failed to fetch Manga Payload. Status code: {response.status_code}"
                    )
                    raise ConnectionError(
                        f"Failed to fetch Manga Payload. Status code: {response.status_code}"
                    )

                try:
                    data = response.json()
                    chapters_info = []

                    for chapter in data.get("data", []):
                        attributes = chapter.get("attributes", {})
                        ChID = chapter.get("id")
                        CHNum = attributes.get(
                            "chapter", "None"
                        )  # Use 'None' if not present
                        VolNum = attributes.get(
                            "volume", "None"
                        )  # Use 'None' if not present
                        TLLang = attributes.get(
                            "translatedLanguage", "None"
                        )  # Use 'None' if not present
                        title = attributes.get("title", "Unknown Title")
                        PublisherName = None  # Default to None if not found

                        # Attempt to get the publisher name if scanlation group is included
                        for relationship in chapter.get("relationships", []):
                            if relationship["type"] == "scanlation_group":
                                PublisherName = relationship["attributes"].get(
                                    "name", "Unknown Publisher"
                                )
                                break  # Exit loop after finding the first scanlation group

                        chapters_info.append(
                            {
                                "ChID": ChID,
                                "CHNum": CHNum,
                                "VolNum": VolNum,
                                "TLLang": TLLang,
                                "title": title,
                                "PublisherName": PublisherName,
                            }
                        )

                    logging.info(
                        f"Successfully fetched chapters for manga ID: {mangaID}. Total chapters fetched: {len(chapters_info)}"
                    )
                    return chapters_info
                except ValueError as json_error:
                    logging.error("Failed to parse Manga Payload as JSON.")
                    raise JSONError("Failed to parse Manga Payload.") from json_error
            except Exception as e:
                logging.error(f"An error occurred while fetching Manga Payload: {e}")
                raise FetchErrorr(
                    f"An error occurred while fetching Manga Payload: {e}"
                )
