import wikipedia
def car_summary_from_wiki(car):
    try:
        car = car.split(" ")[0]
        page = wikipedia.search(car)[0]
        #print(page)
        #print(wikipedia.page(page).content)
        text = wikipedia.page(page).summary
    except:
        text = "Unfortunately, CarClassifier was not able to find any information about this model on Wikipedia. Sorry."
    return text

if __name__ == "__main__":
    car_summary_from_wiki("Acura ILX")