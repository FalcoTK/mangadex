from ..error import NotFoundError, ConnectionError, FetchErrorr
from curl_cffi.requests import Session
import logging
from urllib.parse import quote


class Search:
    """Search manga, author, or group on MangaDex."""

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    async def manga(
        self, title: str, contentRating: str = "all", MaxSearch: int = None
    ):
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
                if contentRating == "all":
                    CntnRate = "contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica"
                if contentRating == "safe":
                    CntnRate = "contentRating[]=safe"
                if contentRating == "suggestive":
                    CntnRate = "contentRating[]=suggestive"
                if contentRating == "erotica":
                    CntnRate = "contentRating[]=erotica"
                if MaxSearch is None:
                    MaxSearch = 5

                logging.info(
                    f"Searching for manga with title: {title} (MaxSearch: {MaxSearch})"
                )

                response = s.get(
                    f"https://api.mangadex.org/manga?title=%20{quote(title)}&limit={MaxSearch}&{CntnRate}&includes[]=cover_art&order[relevance]=desc"
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

    async def RandomSearch(
        self,
        contentRating: str = "all",
    ):
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

                if contentRating == "all":
                    CntnRate = "contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica"
                if contentRating == "safe":
                    CntnRate = "contentRating[]=safe"
                if contentRating == "suggestive":
                    CntnRate = "contentRating[]=suggestive"
                if contentRating == "erotica":
                    CntnRate = "contentRating[]=erotica"

                response = s.get(
                    f"https://api.mangadex.org/manga/random?{CntnRate}&includes[]=artist&includes[]=author&includes[]=cover_art"
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


class AdvanceSearch:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    async def SortBy(
        self,
        Query: str,
        contentRating: str = "all",
        MaxSearch: int = 1,
        Shortby: int = None,
    ):
        """
        Performs an advanced search for manga based on SortBy criteria.

        Args:
            Query (str): The search term or query.
            MaxSearch (int, optional): The maximum number of search results. Default is 1.
            Shortby (int, optional): Defines the sorting method for the search results.
                - None : (default value)
                - 1 : relevance (sorts by relevance to the query).
                - 2 : latestUploadedChapter desc (sorts by the newest uploaded chapter).
                - 3 : latestUploadedChapter asc (sorts by the oldest uploaded chapter).
                - 4 : title asc (sorts by title in ascending order).
                - 5 : title desc (sorts by title in descending order).
                - 6 : rating desc (sorts by highest rating first).
                - 7 : rating asc (sorts by lowest rating first).
                - 8 : followedCount desc (sorts by the most followed manga).
                - 9 : followedCount asc (sorts by the least followed manga).
                - 10: createdAt desc (sorts by the newest creation date).
                - 11: createdAt asc (sorts by the oldest creation date).
                - 12: year asc (sorts by the earliest publication year).
                - 13: year desc (sorts by the latest publication year).
        """
        logging.info(
            f"Starting manga search with query: '{Query}', MaxSearch: {MaxSearch}, Shortby: {Shortby}"
        )

        with Session(impersonate="chrome120") as s:
            try:
                # Define sorting options
                ShortType = {
                    "1": "relevance",
                    "2": "latestUploadedChapter desc",
                    "3": "latestUploadedChapter asc",
                    "4": "title asc",
                    "5": "title desc",
                    "6": "rating desc",
                    "7": "rating asc",
                    "8": "followedCount desc",
                    "9": "followedCount asc",
                    "10": "createdAt desc",
                    "11": "createdAt asc",
                    "12": "year asc",
                    "13": "year desc",
                }

                # Prepare order string based on Shortby
                if Shortby in ShortType and Shortby != "1":
                    order = f"order[{ShortType[str(Shortby)].replace(' ', ']=')}]"
                else:
                    order = ""  # No ordering if Shortby is None or 1

                if contentRating == "all":
                    CntnRate = "contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica"
                if contentRating == "safe":
                    CntnRate = "contentRating[]=safe"
                if contentRating == "suggestive":
                    CntnRate = "contentRating[]=suggestive"
                if contentRating == "erotica":
                    CntnRate = "contentRating[]=erotica"

                # Construct URL
                base_url = "https://api.mangadex.org/manga"
                url = f"{base_url}?limit={MaxSearch}&offset=0&includes[]=cover_art&{CntnRate}&title={quote(Query)}&hasAvailableChapters=true&includedTagsMode=AND&excludedTagsMode=OR"

                if order:
                    url += f"&{order}"

                logging.debug(f"Constructed URL: {url}")
                response = s.get(url)

                # Check for HTTP errors
                response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

                data = response.json()
                logging.info("Received response from MangaDex API.")

                # Check for API errors in response
                if data["result"] == "error":
                    logging.error(
                        "Manga search returned an error: %s",
                        data.get("message", "Unknown error"),
                    )
                    raise ValueError("Manga search returned an error")

                logging.info("Manga search completed successfully.")
                return data  # Return the actual data instead of a placeholder

            except ValueError as ve:
                logging.error("ValueError: %s", str(ve))
                raise

            except Exception as e:
                logging.error(
                    "An unexpected error occurred while fetching manga: %s", str(e)
                )
                raise RuntimeError(
                    f"An unexpected error occurred while fetching manga: {str(e)}"
                )

    async def FilterTags(
        self,
        Query: str,
        Format: int = None,
        Genre: int = None,
        Theme: int = None,
        Content: int = None,
    ):
        TagIdInformation = {
            "Formats": {
                "1": "b11fda93-8f1d-4bef-b2ed-8803d3733170",
                "2": "f4122d1c-3b44-44d0-9936-ff7502c39ad3",
                "3": "51d83883-4103-437c-b4b1-731cb73d786c",
                "4": "0a39b5a1-b235-4886-a747-1d05d216532d",
                "5": "b13b2a48-c720-44a9-9c77-39c9979373fb",
                "6": "7b2ce280-79ef-4c09-9b58-12b7c23a9b78",
                "7": "7b2ce280-79ef-4c09-9b58-12b7c23a9b78",
                "8": "3e2b8dae-350e-4ab8-a8ce-016e844b9f0d",
                "9": "320831a8-4026-470b-94f6-8353740e6f04",
                "10": "0234a31e-a729-4e28-9d6a-3f87c4966b9e",
                "11": "891cf039-b895-47f0-9229-bef4c96eccd4",
                "12": "e197df38-d0e7-43b5-9b09-2842d0c326dd",
            },
            "Genres": {
                "1": "391b0423-d847-456f-aff0-8b0cfc03066b",
                "2": "87cc87cd-a395-47af-b27a-93258283bbc6",
                "3": "5920b825-4181-4a17-beeb-9918b0ff7a30",
                "4": "4d32cc48-9f00-4cca-9b5a-a839f0764984",
                "5": "5ca48985-9a9d-4bd8-be29-80dc0303db72",
                "6": "b9af3a63-f058-46de-a9a0-e0c13906197a",
                "7": "cdc58593-87dd-415e-bbc0-2ec27bf404cc",
                "8": "a3c67850-4684-404e-9b7f-c69850ee5da6",
                "9": "33771934-028e-4cb3-8744-691e866a923e",
                "10": "cdad7e68-1419-41dd-bdce-27753074a640",
                "11": "ace04997-f6bd-436e-b261-779182193d3d",
                "12": "81c836c9-914a-4eca-981a-560dad663e73",
                "13": "50880a9d-5440-4732-9afb-8f457127e836",
                "14": "c8cbe35b-1b2b-4a3f-9c37-db84c4514856",
                "15": "ee968100-4191-4968-93d3-f82d72be7e46",
                "16": "b1e97889-25b4-4258-b28b-cd7f4d28ea9b",
                "17": "3b60b75c-a2d7-4860-ab56-05f391bb889c",
                "18": "423e2eae-a7a2-4a8b-ac03-a8351462d71d",
                "19": "256c8bd9-4904-4360-bf4f-508a76d67183",
                "20": "e5301a23-ebd9-49dd-a0cb-2add944c7fe9",
            },
            "Themes": {
                "1": "e64f6742-c834-471d-8d72-dd51fc02b835",
                "2": "3de8c75d-8ee3-48ff-98ee-e20a65c86451",
                "3": "ea2bc92d-1c26-4930-9b7c-d5c0dc1b6869",
                "4": "9ab53f92-3eed-4e9b-903a-917c86035ee3",
                "5": "da2d50ca-3018-4cc0-ac7a-6b7d472a29ea",
                "6": "39730448-9a5f-48a2-85b0-a70db87b1233",
                "7": "2bd2e8d0-f146-434a-9b51-fc9ff2c5fe6a",
                "8": "3bb26d85-09d5-4d2e-880c-c34b974339e9",
                "9": "fad12b5e-68ba-460e-b933-9ae8318f5b65",
                "10": "aafb99c1-7f60-43fa-b75f-fc9502ce29c7",
                "11": "5bd0e105-4481-44ca-b6e7-7544da56b1a3",
                "12": "2d1f5d56-a1e5-4d0d-a961-2193588b08ec",
                "13": "85daba54-a71c-4554-8a28-9901a8b0afad",
                "14": "a1f53773-c69a-4ce5-8cab-fffcd90b1565",
                "15": "799c202e-7daa-44eb-9cf7-8a3c0441531e",
                "16": "ac72833b-c4e9-4878-b9db-6c8a4a99444a",
                "17": "dd1f77c5-dea9-4e2b-97ae-224af09caf99",
                "18": "36fd93ea-e8b8-445e-b836-358f02b3d33d",
                "19": "f42fbf9e-188a-447b-9fdc-f19dc1e4d685",
                "20": "489dd859-9b61-4c37-af75-5b18e88daafc",
                "21": "92d6d951-ca5e-429c-ac78-451071cbf064",
                "22": "df33b754-73a3-4c54-80e6-1a74a8058539",
                "23": "9467335a-1b83-4497-9231-765337a00b96",
                "24": "0bc90acb-ccc1-44ca-a34a-b9f3a73259d0",
                "25": "65761a2a-415e-47f3-bef2-a9dababba7a6",
                "26": "81183756-1453-4c81-aa9e-f6e1b63be016",
                "27": "caaa44eb-cd40-4177-b930-79d3ef2afe87",
                "28": "ddefd648-5140-4e5f-ba18-4eca4071d19b",
                "29": "eabc5b4c-6aff-42f3-b657-3e90cbd00b75",
                "30": "5fff9cde-849c-4d78-aab0-0d52b2ee1d25",
                "31": "292e862b-2d17-4062-90a2-0356caa4ae27",
                "32": "31932a7e-5b8e-49a6-9f12-2afa39dc544c",
                "33": "d7d1730f-6eb0-4ba6-9437-602cac38664",
                "34": "9438db5a-7e2a-4ac0-b39e-e0d95a34b8a8",
                "35": "d14322ac-4d6f-4e9b-afd9-629d5f4d8a41",
                "36": "8c86611e-fab7-4986-9dec-d1a2f44acdd5",
                "37": "631ef465-9aba-4afb-b0fc-ea10efe274a8",
            },
            "Content": {
                "1": "b29d6a3d-1569-4e7a-8caf-7557bc92cd5d",
                "2": "97893a4c-12af-4dac-b6be-0dffb353568e",
            },
        }

        SearchCategory = {
            "Formats": {
                "1": "Anthology",
                "2": "Award Winning",
                "3": "Doujinshi",
                "4": "Web Comic",
                "5": "4-Koma",
                "6": "Adaptation",
                "7": "Self-Published",
            },
            "Genres": {
                "1": "Fan Colored",
                "2": "Full Color",
                "3": "Long Strip",
                "4": "Official Colored",
                "5": "Oneshot",
                "6": "Action",
                "7": "Adventure",
                "8": "Boys' Love",
                "9": "Comedy",
                "10": "Crime",
                "11": "Drama",
                "12": "Medical",
                "13": "Mystery",
                "14": "Philosophical",
                "15": "Psychological",
                "16": "Romance",
                "17": "Sci-Fi",
                "18": "Fantasy",
                "19": "Girls' Love",
                "20": "Historical",
                "21": "Horror",
                "22": "Slice of Life",
                "23": "Sports",
                "24": "Superhero",
                "25": "Thriller",
                "26": "Isekai",
                "27": "Magical Girls",
                "28": "Mecha",
                "29": "Tragedy",
                "30": "Wuxia",
            },
            "Themes": {
                "1": "Aliens",
                "2": "Animals",
                "3": "Cooking",
                "4": "Crossdressing",
                "5": "Delinquents",
                "6": "Demons",
                "7": "Genderswap",
                "8": "Ghosts",
                "9": "Gyaru",
                "10": "Harem",
                "11": "Incest",
                "12": "Loll",
                "13": "Mafia",
                "14": "Magic",
                "15": "Martial Arts",
                "16": "Military",
                "17": "Monster Girls",
                "18": "Monsters",
                "19": "Music",
                "20": "Ninja",
                "21": "Office Workers",
                "22": "Reverse Harem",
                "23": "Samurai",
                "24": "School Life",
                "25": "Shota",
                "26": "Supernatural",
                "27": "Survival",
                "28": "Time Travel",
                "29": "Police",
                "30": "Post-Apocalyptic",
                "31": "Traditional Games",
                "32": "Vampires",
                "33": "Reincarnation",
                "34": "Video Games",
                "35": "Villainess",
                "36": "Virtual Reality",
                "37": "Zombies",
            },
            "Content": {
                "1": "Gore",
                "2": "Sexual Violence",
            },
        }
        FilteredTags = {
            "Query": Query,
            "Formats": [],
            "Genres": [],
            "Themes": [],
            "Content": [],
        }

        # Add selected Format if provided
        if Format is not None and str(Format) in SearchCategory["Formats"]:
            FilteredTags["Formats"].append(SearchCategory["Formats"][str(Format)])

        # Add selected Genre if provided
        if Genre is not None and str(Genre) in SearchCategory["Genres"]:
            FilteredTags["Genres"].append(SearchCategory["Genres"][str(Genre)])

        # Add selected Theme if provided
        if Theme is not None and str(Theme) in SearchCategory["Themes"]:
            FilteredTags["Themes"].append(SearchCategory["Themes"][str(Theme)])

        # Add selected Content if provided
        if Content is not None and str(Content) in SearchCategory["Content"]:
            FilteredTags["Content"].append(SearchCategory["Content"][str(Content)])
