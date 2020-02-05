from gazpacho import get, Soup

ENDPOINT = 'https://obmenka24.kiev.ua/ua'

def main(ENDPOINT: str):
    response = get(ENDPOINT)
    soup = Soup(response)


if __name__ == '__main__':
    main()
