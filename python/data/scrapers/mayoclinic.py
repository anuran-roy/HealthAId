import ssl
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import aiohttp
import asyncio
import re
import json


def send_request(letter: str) -> list:
    a = requests.get(
        f"https://www.mayoclinic.org/diseases-conditions/index?letter={letter}"
    )
    soup_a = BeautifulSoup(a.text, features="lxml")

    link_elements_list: list[Tag] = soup_a.find_all(
        "a", {"class": "cmp-result-name__link"}
    )
    links_list: list[str] = []

    for ele in link_elements_list:
        links_list.append(ele.attrs.get("href"))

    return links_list


async def send_async_request(
    url, session=aiohttp.ClientSession(conn_timeout=5.0, loop=asyncio.new_event_loop())
):
    async with session.get(url) as response:
        resp = await response.read()

        soup_a = BeautifulSoup(resp.decode("utf-8"), features="lxml")

        link_elements_list: list[Tag] = soup_a.find_all(
            "a", {"class": "cmp-result-name__link"}
        )
        links_list: list = []

        for ele in link_elements_list:
            links_list.append(ele.attrs.get("href"))

        # print(f"Number of Links scraped for url {url} = ", len(links_list))
        return links_list


async def send_requests_parallel(urls_list: list, loop) -> list[str]:
    data = []
    async with aiohttp.ClientSession(conn_timeout=5.0, loop=loop) as session:
        data = await asyncio.gather(
            # map(send_async_request, [session] * len(urls_list), urls_list)
            *[send_async_request(url=url, session=session) for url in urls_list],
            return_exceptions=True,
        )

    return data


async def get_all_links(loop=asyncio.new_event_loop()) -> list[str]:
    letters = [chr(x) for x in range(65, 91)]

    total_links = []

    # for letter in letters:
    #     total_links.extend(send_request(letter))

    index_links = list(
        map(
            lambda letter: f"https://www.mayoclinic.org/diseases-conditions/index?letter={letter}",
            letters,
        )
    )

    total_links = await send_requests_parallel(index_links, loop=loop)
    # print(total_links)
    print("Type of content in links = ", type(total_links[0][0]))
    sanitized_links_by_letter = [
        list(filter(lambda x: x.find("diseases-conditions") != -1, total_links_segment))
        for total_links_segment in total_links
    ]

    sanitized_links = []

    for segment in sanitized_links_by_letter:
        sanitized_links += segment

    # print("\n\n\nLinks = \n\n\n")
    # for total_link_segment in sanitized_links:
    #     print(total_link_segment)

    print("Total number of articles discovered = ", len(sanitized_links))

    return sanitized_links


def fetch_content(url: str) -> str:
    soup: BeautifulSoup = BeautifulSoup(requests.get(url).content, features="lxml")
    soup_data = soup.find_all("div", {"class": "aem-container"})

    return "\n====\n".join(
        [
            "\n---\n".join([x.get_text() for x in soup_element.contents])
            for soup_element in soup_data
        ]
    )


def contents_till_next_section(section: Tag) -> list[str]:
    limit_reached = False
    sections_content = []
    next_section = section
    while not limit_reached:
        next_section = next_section.find_next_sibling()
        if next_section is None or next_section.name == "h2":
            limit_reached = True
        else:
            sections_content.append(next_section.get_text(separator="\n\n", strip=True))

    section_name = section.contents[0] if len(section.contents) > 0 else ""
    sections_data = "\n\n".join([x for x in sections_content if x not in [""]])

    return {section_name.replace(" ", "_"): sections_data}


def get_title_from_url(url: str) -> str:
    url = url[:-1] if url.endswith("/") else url
    regex = "diseases-conditions/.*/"
    match = re.search(regex, url)
    matched_str = url[match.start() : match.end()]
    title = matched_str[matched_str.find("/") + 1 : matched_str.rfind("/")]

    if title.find("/") != -1:
        title = title[: title.find("/")]
    title = title.replace("-", " ")
    title = title.capitalize()

    # print(title)
    return title


def get_data_from_url(url: str):
    content = requests.get(url).content.decode("utf-8")
    soup = BeautifulSoup(content, features="lxml")

    condition_name: str = get_title_from_url(url)
    section_headings = soup.find_all("h2", {"class": "", "data-msg": ""})
    sections_data = list(
        map(
            lambda section_heading: contents_till_next_section(section_heading),
            section_headings,
        )
    )

    total_sections_data = {}

    for section_data in sections_data:
        total_sections_data = total_sections_data | section_data

    # final_data = {condition_name: total_sections_data} # For indexing by disease name
    wanted_sections = [
        "Overview",
        "Symptoms",
        "Causes",
        "Risk_factors",
        "Related",
        "Complications",
        "Prevention",
        "Types",
    ]

    final_data = {}
    for field in wanted_sections:  # total_sections_data.keys():
        # if field in wanted_sections:
        final_data[field] = total_sections_data.get(field)

    final_data = final_data | {"Name": condition_name}  # For listing
    try:
        del final_data[
            condition_name
        ]  # Delete spammy section containing text of entire article, if any.
    except KeyError:
        pass

    return final_data


async def fetch_content_async(
    url_list: list[str], loop=asyncio.new_event_loop()
) -> list[str]:
    contents = []
    soup_entries: list[BeautifulSoup] = []
    # async with aiohttp.ClientSession(conn_timeout=5.0, loop=loop) as session:
    #     contents = await asyncio.gather(*[session.get(url) for url in url_list])

    contents = list(map(requests.get, url_list))
    for content in contents:
        # text: bytes = await content.read()
        # soup_entries.append(BeautifulSoup(text.decode("utf-8"), features="lxml"))
        soup_entries.append(BeautifulSoup(content.content, features="lxml"))

    return [
        "\n\n====\n\n".join(
            list(
                filter(
                    lambda x: x.strip() not in ["", "\n"],
                    [
                        x.get_text(separator="\n----\n", strip=True)
                        for x in soup_data.find_all("article", {"id": "main-content"})
                        # .find("div", {"class": "row"})
                        # .find("div", {"class": "content"})
                        # .children
                    ],
                )
            )
        )
        for soup_data in soup_entries
    ]


def get_data(offset: int = 0, limit: int = -1) -> list[str]:
    loop = asyncio.new_event_loop()
    links_all = sorted(loop.run_until_complete(get_all_links(loop)))
    # contents: dict = {} # For indexing by disease name
    contents: list[dict] = []

    links_filtered = links_all if limit == -1 else links_all[offset : limit + offset]

    print("Number of filtered links = ", len(links_filtered))
    for link in links_filtered:
        # print("Getting data from = ", link)
        # contents = contents | get_data_from_url(link) # For indexing by disease name
        contents.append(get_data_from_url(link))
    return contents


if __name__ == "__main__":
    # file = open("a.json", "w") # For indexing by disease name
    from db.postgres.db import db
    from db.postgres.models.models import MayoClinicEntry
    from time import sleep

    LIMIT = 20
    INDEX_COUNT = 1146

    def write_to_db(json_data: list[dict]):
        entry = MayoClinicEntry.insert_many(json_data).execute()

    # file = open("b.json", "w")  # For listing
    # file.write(json.dumps(get_data(offset=10, limit=LIMIT), indent=4))
    # file.close()

    for offset in range(0, INDEX_COUNT, LIMIT):
        write_to_db(
            list(
                filter(
                    lambda x: x
                    != {
                        "Overview": None,
                        "Symptoms": None,
                        "Causes": None,
                        "Risk_factors": None,
                        "Related": None,
                        "Complications": None,
                        "Prevention": None,
                        "Types": None,
                        "Name": None,
                    },
                    get_data(offset=offset, limit=LIMIT),
                )
            )
        )
        sleep(5.0)
        asyncio.sleep(5.0)
