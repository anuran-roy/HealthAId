import requests
from bs4 import BeautifulSoup, Tag
# from utils.elasticsearch import send_to_elasticsearch
# from db.elasticsearch import db

def get_soup_items_from_search(search_query: str):
    soup = BeautifulSoup(requests.get(f"https://www.drugs.com/search.php?searchterm={search_query}").content)
    soup_items = []
    soup_components = soup.find_all("a", {"class": "ddc-search-result-link-wrap"})
    for soup in soup_components:
        title = soup.find("h3", {"class": "ddc-media-title"})
        soup_items.append((title.get_text(), soup.attrs.get("href")))
        print(title.get_text())

    return soup_items

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

    section_name = section.attrs.get("id")
    section_name = section_name.capitalize().replace("-", " ") if section_name is not None else None
    if section_name is None:
        section_name = section.contents[0] if len(section.contents) > 0 else ""
    sections_data = "\n\n".join([x for x in sections_content if x not in [""]])

    return {section_name: sections_data}

def extract_info(sp: BeautifulSoup):
    cnts = sp.find_all("h2", {"class": "ddc-anchor-offset"})
    sections = list(map(lambda x: contents_till_next_section(x), cnts))

    total_data = {}
    for section in sections:
        total_data = total_data | section

    print(total_data)
    return total_data

# contnt = requests.get(
#     # "https://www.drugs.com/ibuprofen.html"
#     "https://www.drugs.com/mounjaro.html"
# ).content

# sp = BeautifulSoup(contnt)

# sp.prettify()

# extract_info(sp)

def get_data(search: str):
    data = get_soup_items_from_search(search_query=search)
    print(data)
    most_relevant_link = data[0][1]
    link_data = BeautifulSoup(requests.get(most_relevant_link).content)

    extracted_info = extract_info(link_data)
    print("Extracted info from drugs.com: ", extracted_info)

    # send_to_elasticsearch(db.client, [extracted_info], index="drugs_com_index")
    return extracted_info

if __name__ == "__main__":
    get_data("Diclofenac")