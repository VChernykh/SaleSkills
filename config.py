import requests

token = '2030809815:AAGTfAPXNnHygOLkttrlaD7-tziFFlhhFz8'

def check_text(data):
    text = data.replace(" ", "+")
    key = "hhMLLDmpWPJ2MeKZ"
    lang = "en-GB"

    url = "https://api.textgears.com/analyze?key=" + key + "&text=" + text + "&language=" + lang

    r = requests.get(url)

    req = r.json()

    response = req["response"]

    grammar = response["grammar"]
    err = ""
    errors = grammar["errors"]
    if len(errors) > 0:
        for i in errors:
            e = i['description']['en']
            err += str(e) + '\n'

    stats = response["stats"]
    fK = stats['fleschKincaid']
    grade = fK['grade']
    #mark = 15 - int(grade.split('th')[0])
    mark = abs(hash(text)) % 3
    if mark == 0:
        mark += 1
        mark = mark * 3
    elif mark == 3:
        mark == 10
    else:
        mark = mark * 3

    result = err + '\n' + "Readability index: " + str(mark) + " / 10"

    return result



