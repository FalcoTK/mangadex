<div align="center">
<pre>
  MangaDex - UnOfficial API Wrapper
</div>

# 💬 MangaDex - UnOfficial API Wrapper

**MangaDex - UnOfficial API Wrapper** is a powerful Python library tailored to interact seamlessly with the [MangaDex API](https://api.mangadex.org/). This library offers an intuitive interface for searching manga titles, retrieving chapter details, and handling media assets like cover images. It includes error handling and logging, ensuring reliable integration into your projects.

---

### 🚀 Features

- **Manga Search**: Search for manga titles by name, with content rating filters and cover art inclusion options.
- **Group Search**: Retrieve manga groups by name, including details like social media links.
- **Author Search**: Fetch authors by name and retrieve biographies along with social media profiles.
- **Error Handling**: Custom exceptions to provide reliable and informative error management.
- **Modular Architecture**: Designed for scalability and maintainability, making it easy to extend or modify for specific needs.

---

### 🛠️ Installation

To install the package:

```bash
pip install mangadex-wrapper
```

## ❓ Documentation & Examples

### Manga Search:

```python
from mangadex_wrapper import Search

# Initialize the search object
search = Search()

# Search for a manga by title
manga_results = await search.manga("Naruto")

# Display the search results
for manga in manga_results:
    print(f"Manga ID: {manga['id']}, Title: {manga['title']}")
```

### Group Search:

```python
from mangadex_wrapper import Search

# Initialize the search object
search = Search()

# Search for a scanlation group by name
group_results = await search.GroupSearch("Some Group")

# Display the results
for group in group_results:
    print(f"Group Name: {group['name']}, ID: {group['id']}")
```

### Author Search:

```python
from mangadex_wrapper import Search

# Initialize the search object
search = Search()

# Search for an author by name
author_results = await search.author("Eiichiro Oda")

# Display the results
for author in author_results:
    print(f"Author Name: {author['name']}, ID: {author['id']}")
```

---

### 🔍 Advanced Search

The advanced search allows filtering manga by various criteria such as tags, content rating, demographic, chapter availability, and sorting options.

#### Available Filters

- **Content Rating**: Filter manga by rating (`safe`, `suggestive`, `erotica`, or `all`).
- **Tags**: Filter manga by tags (e.g., `action`, `romance`, `comedy`).
- **Demographic**: Filter manga by demographic (`shounen`, `seinen`, `josei`, etc.).
- **Available Chapters**: Filter manga with or without chapters.
- **Sorting**: Sort results by `relevance`, `latest upload`, `year`, or `title`.

#### Sorting Information:

```
1: relevance
2: latestUploadedChapter desc
3: latestUploadedChapter asc
4: title asc
5: title desc
6: rating desc
7: rating asc
8: followedCount desc
9: followedCount asc
10: createdAt desc
11: createdAt asc
12: year asc
13: year desc
```

#### Example Usage

```python
from mangadex_wrapper import Search

# Initialize the search object
search = Search()

# Perform an advanced search
results = await search.AdvancedSearch(
    contentRating="safe",           # Filter by 'safe' content rating
    tags=["action", "adventure"],   # Include manga tagged 'action' and 'adventure'
    demographic="shounen",          # Filter for 'shounen' demographic
    hasAvailableChapters=True,      # Include only manga with available chapters
    sortBy=1,                       # Sort by relevance
    MaxSearch=10                    # Limit results to 10
)

# Display search results
for manga in results:
    print(f"Manga ID: {manga['id']}, Title: {manga['title']}")
```

---

## 📚 Documentation & Examples:

- **Detailed Documentation**: 📚 _Coming soon!_ Comprehensive documentation covering advanced features like chapter fetching and image retrieval.
- **Code Samples**: 🚀 _Coming soon!_ Sample projects to demonstrate how the wrapper can be integrated into your workflows.

## 🏅 Community

This project is under active development, and your feedback is greatly appreciated! Join our [Discord community](https://discord.gg/xxaA8eKMvM) for updates, feature requests, or support.

## ♥️ Support

If this project has helped you, consider giving it a ⭐ on GitHub and sharing it with others! Your support keeps the project alive.

---

### © Copyright

All manga data and media are provided by **MangaDex**, a free and open platform. Special thanks to MangaDex for offering such a comprehensive manga database, and supporting the community.
