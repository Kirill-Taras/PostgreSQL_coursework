from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


employers = {
    "Тинькофф": 78638,
    "Яндекс": 1740,
    "МТС": 3776,
    "ТЕЛЕ2": 4219,
    "Kaspersky": 1057,
    "Goodline": 609089,
    "Сбербанк": 3529,
    "Билайн": 4934,
    "Мегафон": 3127,
    "Ozon": 2180
}
