import requests
from bs4 import BeautifulSoup
import re


def scrape_hotels(city,checkin_date,checkout_date):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5042.108 Safari/537.36"}
    url = f"https://www.booking.com/searchresults.en-gb.html?ss={city}%2C+India&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaGyIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgO4At7VubEGwAIB0gIkMmEzZDU5ZTEtYTUyNC00OWMyLWEyMjEtYzU3NGNiNWRhNjAw2AIG4AIB&sid=a99766448770fcbb30fbeb785a4edea5&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=-2090174&dest_type=city&checkin={checkin_date}&checkout={checkout_date}&group_adults=2&no_rooms=1&group_children=1&age=1&nflt=class%3D5"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    hotel_results = []

    for el in soup.find_all("div", {"data-testid": "property-card"}):
        hotel_results.append({
                "name": el.find("div", {"data-testid": "title"}).text.strip(),
                "link": el.find("a", {"data-testid": "title-link"})["href"],
                "location": el.find("span", {"data-testid": "address"}).text.strip(),
                "pricing": el.find("span", {"data-testid": "price-and-discounted-price"}).text.strip(),
                "rating": el.find("div", {"data-testid": "review-score"}).text.strip().split(" ")[0],
                "review_count": el.find("div", {"data-testid": "review-score"}).text.strip().split(" ")[1],
                "thumbnail": el.find("img", {"data-testid": "image"})['src'],
            })


    return hotel_results


def filter_hotels(hotels):
    filtered_hotels = [hotel for hotel in hotels if float(hotel["rating"].split("Scored")[0]) >= 8 ]
    return filtered_hotels


def find_lowest_price(hotels):
    key_to_replace = "pricing"
    pattern = r'\d{1,3}(?:,\d{3})*'
    for hotel in hotels:
        if key_to_replace in hotel:
            hotel[key_to_replace] =  int(re.sub(r'\D', '', hotel[key_to_replace] ))
    lowest_price = min(hotels, key=lambda x: x["pricing"])
    return lowest_price


city = "Bangalore"  # Example city
checkin_date = '2024-05-25'
checkout_date = '2024-05-31'
hotels = scrape_hotels(city,checkin_date,checkout_date)
filtered_hotels = filter_hotels(hotels)
lowest_price_hotel = find_lowest_price(filtered_hotels)

print("Lowest Price Hotel:")
print("Name:", lowest_price_hotel["name"])
print("Rating:", lowest_price_hotel["rating"].split("Scored")[0])
print("Price:", lowest_price_hotel["pricing"],"INR")
