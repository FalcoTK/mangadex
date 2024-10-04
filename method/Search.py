from ..error import NotFoundError, ConnectionError, FetchErrorr
from ..data.TagId import TagAdvance
from curl_cffi.requests import Session
import logging
from urllib.parse import quote


class Search:
    """
    # COPPYRIGHT MANGA, PROVIDER `MANGADEX <https://mangadex.org/>`_
    Search manga, author, or group on MangaDex."""

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    async def manga(
        self, title: str, contentRating: str = "all", MaxSearch: int = None
    ):
        """
        ### COPPYRIGHT MANGA, PROVIDER `MANGADEX <https://mangadex.org/>`_
        Search for manga by title.

        This method queries the MangaDex API to find manga based on the specified title
        and returns relevant information about the manga.

        Parameters:

            title (str):
                The title of the manga to search for.

            contentRating (str, optional):
                The content rating filter for the search. Options are:
                    - "all": Includes all content ratings.
                    - "safe": Only includes safe content.
                    - "suggestive": Includes suggestive content.
                    - "erotica": Includes erotic content.
                    - Defaults to "all".

            MaxSearch (int, optional):
                The maximum number of results to return. Defaults to 5 if not specified.

        Returns:
            dict: A list of dictionaries containing manga information, where each dictionary includes:
                - id: str, the ID of the manga
                - title: str, the title of the manga
                - altTitles: list, alternative titles of the manga
                - description: str, the description of the manga
                - year: int, the year the manga was published (if available)
                - tags: list, tags associated with the manga
                - status: str, the current status of the manga
                - CoverSmall: str, URL of the small cover image
                - CoverLarge: str, URL of the large cover image

        Raises:
            ConnectionError:
                If the request to the API fails, indicated by a non-200 status code.

            FetchErrorr:
                If there is an error in fetching the manga data from the API.

        Example:
        --------
        ```python
        search = Search()
        manga_results = await search.manga("Naruto")
        for manga in manga_results:
            print(f"Manga ID: {manga['id']}, Title: {manga['title']}")
        ```

        This example searches for manga with the title "Naruto" and prints the ID and title of each found manga.
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
                    details = data["errors"][0]
                    ErrorStatus = details.get("status", "Unknown")
                    ErorrTitle = details.get("title", "Unknown Error")
                    detail = details.get("detail", "No details provided")
                    IDErr = details.get("id", "Unknown ID")
                    logging.error(
                        f"Error [{ErrorStatus}] {ErorrTitle}: {detail} (ID: {IDErr})"
                    )
                    raise FetchErrorr(ErrorStatus, ErorrTitle, detail, IDErr)

                MangaList = []
                for manga in data["data"]:
                    manga_id = manga["id"]
                    cover_art = next(
                        (
                            rel
                            for rel in manga["relationships"]
                            if rel["type"] == "cover_art"
                        ),
                        None,
                    )
                    cover_id = (
                        cover_art["attributes"]["fileName"]
                        if cover_art
                        else "default_cover.jpg"
                    )

                    MangaInfo = {
                        "id": manga_id,
                        "title": manga["attributes"]["title"].get(
                            "en", "Unknown Title"
                        ),
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
                        "CoverSmall": (
                            f"https://mangadex.org/covers/{manga_id}/{cover_id}.256.jpg"
                            if cover_id
                            else None
                        ),
                        "CoverLarge": (
                            f"https://mangadex.org/covers/{manga_id}/{cover_id}"
                            if cover_id
                            else None
                        ),
                    }

                logging.info(f"Found {len(MangaList)} manga entries.")
                return MangaInfo

            except Exception as e:
                logging.error(f"An error occurred while fetching manga: {e}")
                raise FetchErrorr(f"An error occurred while fetching manga: {e}")

    async def author(self, AuthorName: str, MaxSearch: int = None):
        """
        ### COPPYRIGHT MANGA, PROVIDER `MANGADEX <https://mangadex.org/>`_
        Search for authors by name.

        This method queries the MangaDex API to find authors based on the specified author name
        and returns relevant information about the authors.

        Parameters:
            AuthorName (str):
                The name of the author to search for.

        MaxSearch: int, optional
            The maximum number of results to return. Defaults to 5. If None, it will return 5 results.

        Returns:
            dict: A dictionary containing information about the Author, including:
                - id: str, the ID of the author
                - name: str, the name of the author
                - biography: dict, the biography of the author (if available)
                - social_media: dict, a dictionary of social media links related to the author (if available)

        Raises:
            ConnectionError:
                If the request to the API fails, indicated by a non-200 status code.

            FetchErrorr:
                If there is an error in fetching the author data from the API.

        Example:
        --------
        ```python
        author_results = await author(AuthorName="John Doe")
        for author in author_results:
            print(f"Author ID: {author['id']}, Name: {author['name']}")
        ```

        This example searches for authors with the name "John Doe" and prints the ID and name of each found author.
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
                    details = data["errors"][0]
                    ErrorStatus = details.get("status", "Unknown")
                    ErorrTitle = details.get("title", "Unknown Error")
                    detail = details.get("detail", "No details provided")
                    IDErr = details.get("id", "Unknown ID")
                    logging.error(
                        f"Error [{ErrorStatus}] {ErorrTitle}: {detail} (ID: {IDErr})"
                    )
                    raise FetchErrorr(ErrorStatus, ErorrTitle, detail, IDErr)

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
        ### COPPYRIGHT MANGA, PROVIDER `MANGADEX <https://mangadex.org/>`_
        Search for groups by name.

        This method queries the MangaDex API to find groups based on the specified group name
        and returns relevant information about the groups.


        Parameters:
            MaxSearch (int, optional): The maximum number of manga entries to return. Defaults to 1.

        Returns:
            dict: A dictionary containing information about the Group, including:
                - id (str): The ID of the manga.
                - name: str, the name of the group
                - altNames: list of str, alternative names for the group
                - SocialMedia: dict, a dictionary of social media links related to the group (if available)

        Raises:
            ConnectionError:
                If the response status code is not 200, indicating a failure in fetching data from the API.

        Example:
        --------
        ```python
        group_results = await GroupSearch(GroupName="Scanlation Group")
        for group in group_results:
            print(f"Group ID: {group['id']}, Name: {group['name']}, Alt Names: {group['altNames']}")
        ```

        This example searches for groups with the name "Scanlation Group" and prints the ID, name, and alternative names of each found group.
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
                    details = data["errors"][0]
                    ErrorStatus = details.get("status", "Unknown")
                    ErorrTitle = details.get("title", "Unknown Error")
                    detail = details.get("detail", "No details provided")
                    IDErr = details.get("id", "Unknown ID")
                    logging.error(
                        f"Error [{ErrorStatus}] {ErorrTitle}: {detail} (ID: {IDErr})"
                    )
                    raise FetchErrorr(ErrorStatus, ErorrTitle, detail, IDErr)

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
        ### COPPYRIGHT MANGA, PROVIDER `MANGADEX <https://mangadex.org/>`_
        Fetches a random manga and retrieves its ID, title, alternative titles, and description.

        Parameters:
            MaxSearch (int, optional): The maximum number of manga entries to return. Defaults to 1.

        Returns:
            dict: A dictionary containing information about the found manga, including:
                - id (str): The ID of the manga.
                - title (str): The title of the manga.
                - altTitles (list): A list of alternate titles.
                - description (str): A description of the manga.
                - year (int): The year the manga was published.
                - tags (list): A list of tags associated with the manga.
                - status (str): The current status of the manga.
                - CoverSmall (str): URL to a small cover image of the manga.
                - CoverLarge (str): URL to a large cover image of the manga.


        Raises:
        -------
        ConnectionError
            If the response status code is not 200, indicating a failure in fetching data from the API.

        NotFoundError
            If the manga search returns an error indicating that no manga could be found.

        FetchErrorr
            For other general errors during the fetch process, including network issues and unexpected responses.

        Example:
        --------
        ```python
        random_manga = await RandomSearch(contentRating="safe")
        print(random_manga)
        ```
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
                    details = data["errors"][0]
                    ErrorStatus = details.get("status", "Unknown")
                    ErorrTitle = details.get("title", "Unknown Error")
                    detail = details.get("detail", "No details provided")
                    IDErr = details.get("id", "Unknown ID")
                    logging.error(
                        f"Error [{ErrorStatus}] {ErorrTitle}: {detail} (ID: {IDErr})"
                    )
                    raise FetchErrorr(ErrorStatus, ErorrTitle, detail, IDErr)
                manga = data["data"]
                mangaID = manga["id"]
                cover_art = next(
                    (
                        rel
                        for rel in manga["relationships"]
                        if rel["type"] == "cover_art"
                    ),
                    None,
                )
                cover_id = (
                    cover_art["attributes"]["fileName"]
                    if cover_art
                    else "default_cover.jpg"
                )
                MangaInfo = {
                    "id": mangaID,
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
                    "CoverSmall": (
                        f"https://mangadex.org/covers/{mangaID}/{cover_id}.256.jpg"
                        if cover_id
                        else None
                    ),
                    "CoverLarge": (
                        f"https://mangadex.org/covers/{mangaID}/{cover_id}"
                        if cover_id
                        else None
                    ),
                }

                logging.info("Successfully fetched random manga.")
                return MangaInfo

            except Exception as e:
                logging.error(f"An error occurred while fetching manga: {e}")
                raise FetchErrorr(f"An error occurred while fetching manga: {e}")

    async def AdvanceSearch(
        self,
        Query: str = None,
        *,
        TagName=None,  # Can now be a string or a list
        SearchByAuthor: str = None,
        MaxSearch: int = 1,
        contentRating: str = "all",
        Demographic=None,
        HasAvailableChapters: bool = True,
        Shortby: int = None,
    ) -> dict[str, any]:
        """
        ### COPPYRIGHT MANGA, PROVIDER `MANGADEX <https://mangadex.org/>`_
        Performs an advanced search for manga based on filtering and sorting criteria.

        Parameters:
            Query (str, optional): A search string for the title of the manga. Defaults to None.
            TagName (str or list, optional): A tag or a list of tags to filter the manga. Defaults to None.
            SearchByAuthor (str, optional): The name of the author to search for. Defaults to None.
            MaxSearch (int, optional): The maximum number of manga entries to return. Defaults to 1.
            contentRating (str, optional): The content rating filter.
                Options: "all", "safe", "suggestive", "erotica". Defaults to "all".
            Demographic (str, optional): The demographic filter.
                Options: None, "all", "shoujo", "shounen", "seinen", "josei". Defaults to None.
            HasAvailableChapters (bool, optional): Whether to include only manga with available chapters. Defaults to True.
            Shortby (int, optional): The sorting order for the results.
                Options: 1 to 13 corresponding to different sorting criteria. Defaults to None, or you can use this:
                    - 1: relevance
                    - 2: latestUploadedChapter desc
                    - 3: latestUploadedChapter asc
                    - 4: title asc
                    - 5: title desc
                    - 6: rating desc
                    - 7: rating asc
                    - 8: followedCount desc
                    - 9: followedCount asc
                    - 10: createdAt desc
                    - 11: createdAt asc
                    - 12: year asc
                    - 13: year desc

        Returns:
            dict: A dictionary containing information about the found manga, including:
                - id (str): The ID of the manga.
                - title (str): The title of the manga.
                - altTitles (list): A list of alternate titles.
                - description (str): A description of the manga.
                - year (int): The year the manga was published.
                - tags (list): A list of tags associated with the manga.
                - status (str): The current status of the manga.
                - CoverSmall (str): URL to a small cover image of the manga.
                - CoverLarge (str): URL to a large cover image of the manga.

        Raises:
            FetchErrorr: If there is an error fetching data from the API or processing the results.

        Example:
        --------
        ```python
        manga_search = await AdvanceSearch(
            Query="One Piece",
            TagName=["Adventure", "Fantasy"],
            SearchByAuthor="Eiichiro Oda",
            MaxSearch=5,
            contentRating="safe",
            Demographic="shounen",
            HasAvailableChapters=True,
            Shortby=2
        )
        print(manga_search)
        """
        try:

            ContentRattingVelue = {
                "all": "contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica",
                "safe": "contentRating[]=safe",
                "suggestive": "contentRating[]=suggestive",
                "erotica": "contentRating[]=erotica",
            }
            DemographicVelue = {
                None: "publicationDemographic[]=none",
                "all": "publicationDemographic[]=shoujo&publicationDemographic[]=seinen&publicationDemographic[]=shounen&publicationDemographic[]=josei&publicationDemographic[]=none",
                "shoujo": "publicationDemographic[]=shoujo",
                "shounen": "publicationDemographic[]=shounen",
                "seinen": "publicationDemographic[]=seinen",
                "josei": "publicationDemographic[]=josei",
            }
            CntnRate = ContentRattingVelue.get(contentRating, "")
            DemographicRTN = DemographicVelue.get(Demographic, "")
            lowertrue = str(HasAvailableChapters).lower()
            includedTags = None
            IdAuthor = None
            order = None

            if SearchByAuthor != None:
                SearchAuthor = await self.author(AuthorName=SearchByAuthor, MaxSearch=1)
                print(SearchAuthor)
                try:
                    IdAuthor = SearchAuthor[0].get("id")
                except Exception as e:
                    logging.error(f"Error fetching author ID: {e}")
                    raise FetchErrorr(f"Error fetching author ID: {e}")

            if Shortby and Shortby != 1:
                velueShort = await TagAdvance().ShortTypeID(Shortby)
                order = f"order[{velueShort.replace(' ', ']=')}]"

            if TagName:
                if isinstance(TagName, str):
                    TagName = [TagName]
                includedTags = "includedTags[]=" + "&includedTags[]=".join(
                    await TagAdvance().FilterTagsID(TagName)
                )

            BaseURL = "https://api.mangadex.org/manga"
            url = (
                f"{BaseURL}?limit={MaxSearch}&offset=0&includes[]=cover_art&{CntnRate}"
                f"&hasAvailableChapters={lowertrue}&includedTagsMode=AND&excludedTagsMode=OR&{DemographicRTN}"
            )

            if includedTags != None:
                url += f"&{includedTags}"
            if Query:
                url += f"&title={quote(Query)}"
            if order != None:
                url += f"&{order}"
            if IdAuthor != None:
                url += f"&artists[]={IdAuthor}"

            # Fetch data
            with Session(impersonate="chrome120") as s:
                response = s.get(url)
                response.raise_for_status()
                data = response.json()

                if data["result"] == "error":
                    details = data["errors"][0]
                    raise FetchErrorr(
                        details.get("status", "Unknown"),
                        details.get("title", "Unknown Error"),
                        details.get("detail", "No details provided"),
                        details.get("id", "Unknown ID"),
                    )

                MangaList = []
                for manga in data["data"]:
                    manga_id = manga["id"]
                    cover_art = next(
                        (
                            rel
                            for rel in manga["relationships"]
                            if rel["type"] == "cover_art"
                        ),
                        None,
                    )
                    cover_id = (
                        cover_art["attributes"]["fileName"]
                        if cover_art
                        else "default_cover.jpg"
                    )

                    MangaInfo = {
                        "id": manga_id,
                        "title": manga["attributes"]["title"].get(
                            "en", "Unknown Title"
                        ),
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
                        "CoverSmall": (
                            f"https://mangadex.org/covers/{manga_id}/{cover_id}.256.jpg"
                            if cover_id
                            else None
                        ),
                        "CoverLarge": (
                            f"https://mangadex.org/covers/{manga_id}/{cover_id}"
                            if cover_id
                            else None
                        ),
                    }

                logging.info(f"Found {len(MangaList)} manga entries.")
                return MangaInfo

        except Exception as e:
            logging.error(f"An error occurred while performing advanced search: {e}")
            raise FetchErrorr(
                f"An error occurred while performing advanced search: {e}"
            )
