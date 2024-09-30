from ..error import NotFoundError, ConnectionError, FetchErrorr
from curl_cffi.requests import Session
import logging
from urllib.parse import quote


class Search:
    """Search manga, author, or group on MangaDex."""

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    async def manga(self, title: str, MaxSearch: int = None):
        """
        Search for manga by title.

        Args:
            title (str): The title of the manga to search for.
            MaxSearch (int, optional): The maximum number of results to return. Defaults to 5.

                                       If the fetch fails, consider decreasing MaxChapters.

        Returns:
            List[Dict]: A list of dictionaries containing manga information.

        Raises:
            ConnectionError: If the request to the API fails.
            FetchErrorr: If there is an error in fetching the manga data.
        """
        with Session(impersonate="chrome120") as s:
            try:
                if MaxSearch is None:
                    MaxSearch = 5

                logging.info(
                    f"Searching for manga with title: {title} (MaxSearch: {MaxSearch})"
                )

                response = s.get(
                    f"https://api.mangadex.org/manga?title=%20{quote(title)}&limit={MaxSearch}&contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&includes[]=cover_art&order[relevance]=desc"
                )

                if response.status_code != 200:
                    logging.error(
                        f"Failed to fetch manga. Status code: {response.status_code}"
                    )
                    raise ConnectionError(
                        f"Failed to fetch manga. Status code: {response.status_code}"
                    )

                data = response.json()

                if data["result"] == "error":
                    logging.error("Manga search returned an error.")
                    raise NotFoundError("Something went wrong")

                # Extract relevant manga information
                MangaList = []
                for manga in data["data"]:
                    MangaInfo = {
                        "id": manga["id"],
                        "title": manga["attributes"]["title"]["en"],
                        "altTitles": [
                            Alt["en"]
                            for Alt in manga["attributes"]["altTitles"]
                            if "en" in Alt
                        ],
                        "description": manga["attributes"]["description"].get("en", ""),
                        "year": manga["attributes"]["year"],
                        "tags": [
                            tag["attributes"]["name"]["en"]
                            for tag in manga["attributes"]["tags"]
                        ],
                        "status": manga["attributes"]["status"],
                    }
                    MangaList.append(MangaInfo)

                logging.info(f"Found {len(MangaList)} manga entries.")
                return MangaList

            except Exception as e:
                logging.error(f"An error occurred while fetching manga: {e}")
                raise FetchErrorr(f"An error occurred while fetching manga: {e}")

    async def author(self, AuthorName: str, MaxSearch: int = None):
        """
        Search for authors by name.

        Args:
            AuthorName (str): The name of the author to search for.
            MaxSearch (int, optional): The maximum number of results to return. Defaults to 5.

                                       If the fetch fails, consider decreasing MaxChapters.

        Returns:
            List[Dict]: A list of dictionaries containing author information.

        Raises:
            ConnectionError: If the request to the API fails.
            FetchErrorr: If there is an error in fetching the manga data.
        """
        with Session(impersonate="chrome120") as s:
            try:
                if MaxSearch is None:
                    MaxSearch = 5

                logging.info(
                    f"Searching for author with name: {AuthorName} (MaxSearch: {MaxSearch})"
                )

                response = s.get(
                    f"https://api.mangadex.org/author?name={quote(AuthorName)}&limit={MaxSearch}"
                )

                if response.status_code != 200:
                    logging.error(
                        f"Failed to fetch author. Status code: {response.status_code}"
                    )
                    raise ConnectionError(
                        f"Failed to fetch author. Status code: {response.status_code}"
                    )

                data = response.json()

                if data["result"] == "error":
                    logging.error("Author search returned an error.")
                    raise NotFoundError("Something went wrong")

                # Extract relevant author information
                AuthorList = []
                for author in data["data"]:
                    AuthorInfo = {
                        "id": author["id"],
                        "name": author["attributes"]["name"],
                        "biography": author["attributes"].get("biography", {}),
                        "social_media": {},
                    }

                    SocialMedia = [
                        "twitter",
                        "pixiv",
                        "melonBook",
                        "fanBox",
                        "booth",
                        "namicomi",
                        "nicoVideo",
                        "skeb",
                        "fantia",
                        "tumblr",
                        "youtube",
                        "weibo",
                        "naver",
                        "website",
                    ]

                    for field in SocialMedia:
                        value = author["attributes"].get(field)
                        # Include only if the value is not None and not empty
                        if value is not None and value != "None":
                            AuthorInfo["social_media"][field] = value

                    AuthorList.append(AuthorInfo)

                logging.info(f"Found {len(AuthorList)} author entries.")
                return AuthorList

            except Exception as e:
                logging.error(f"An error occurred while fetching author: {e}")
                raise FetchErrorr(f"An error occurred while fetching author: {e}")

    async def GroupSearch(self, GroupName: str, MaxSearch: int = None):
        """
        Search for groups by name.

        Args:
            GroupName (str): The name of the group to search for.
            MaxSearch (int, optional): The maximum number of results to return. Defaults to 5.


                                       If the fetch fails, consider decreasing MaxChapters.

        Returns:
            List[Dict]: A list of dictionaries containing group information.

        Raises:
            ConnectionError: If the request to the API fails.
            FetchErrorr: If there is an error in fetching the manga data.
        """
        with Session(impersonate="chrome120") as s:
            try:
                if MaxSearch is None:
                    MaxSearch = 5

                logging.info(
                    f"Searching for group with name: {GroupName} (MaxSearch: {MaxSearch})"
                )

                response = s.get(
                    f"https://api.mangadex.org/group?name={quote(GroupName)}&limit={MaxSearch}&includes[]=leader"
                )

                if response.status_code != 200:
                    logging.error(
                        f"Failed to fetch Group. Status code: {response.status_code}"
                    )
                    raise ConnectionError(
                        f"Failed to fetch Group. Status code: {response.status_code}"
                    )

                data = response.json()

                if data["result"] == "error":
                    logging.error("Group search returned an error.")
                    raise NotFoundError("Something went wrong")

                GroupList = []
                for group in data["data"]:
                    GroupInfo = {
                        "id": group["id"],
                        "name": group["attributes"]["name"],
                        "altNames": group["attributes"].get("altNames", []),
                        "social_media": {},
                    }

                    # Check for social media links and include them if they exist
                    SocialMedia = [
                        "website",
                        "ircServer",
                        "ircChannel",
                        "discord",
                        "contactEmail",
                        "twitter",
                        "mangaUpdates",
                    ]

                    for field in SocialMedia:
                        value = group["attributes"].get(field)
                        # Include only if the value is not None and not empty
                        if value is not None and value != "None":
                            GroupInfo["social_media"][field] = value

                    GroupList.append(GroupInfo)

                logging.info(f"Found {len(GroupList)} group entries.")
                return GroupList

            except Exception as e:
                logging.error(f"An error occurred while fetching group: {e}")
                raise FetchErrorr(f"An error occurred while fetching group: {e}")

    async def RandomSearch(self):
        """
        Fetches a random manga and retrieves its ID, title, alternative titles, and description.

        Returns:
            Dict[str, Any]: A dictionary containing the manga ID, title, alternative titles, and description.

        Raises:
            ConnectionError: If the response status code is not 200.
            NotFoundError: If the manga search returns an error.
            FetchErrorr: For other general errors during the fetch process.
        """
        with Session(impersonate="chrome120") as s:
            try:
                logging.info(f"Searching for Random manga")

                response = s.get(
                    "https://api.mangadex.org/manga/random?contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&includes[]=artist&includes[]=author&includes[]=cover_art"
                )

                if response.status_code != 200:
                    logging.error(
                        f"Failed to fetch Random Manga. Status code: {response.status_code}"
                    )
                    raise ConnectionError(
                        f"Failed to fetch Radnom Manga. Status code: {response.status_code}"
                    )

                data = response.json()

                if data["result"] == "error":
                    logging.error("Manga search returned an error.")
                    raise NotFoundError("Something went wrong")

                manga = data["data"]
                MangaInfo = {
                    "id": manga["id"],
                    "title": manga["attributes"]["title"]["en"],
                    "altTitles": [
                        alt_title["en"]
                        for alt_title in manga["attributes"].get("altTitles", [])
                        if "en" in alt_title
                    ],
                    "description": manga["attributes"]["description"].get("en", ""),
                    "year": manga["attributes"].get("year", None),
                    "tags": [
                        tag["attributes"]["name"]["en"]
                        for tag in manga["attributes"].get("tags", [])
                    ],
                    "status": manga["attributes"].get("status", "Unknown"),
                }

                logging.info("Successfully fetched random manga.")
                return MangaInfo

            except Exception as e:
                logging.error(f"An error occurred while fetching manga: {e}")
                raise FetchErrorr(f"An error occurred while fetching manga: {e}")
