import pandas as pd
from datetime import datetime

sheet_id = "1FV3cg92TdBCH9T2vxhLlA5qSdfgQrkik9f6qKJ7ZyaI"
sheet_name = "OKED"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"


class Person:
    def __init__(self, name, surname, patronymic, city, organisation):
        self.name = name
        self.surname = surname
        if isinstance(patronymic, str):
            self.patronymic = patronymic
        else:
            self.patronymic = ""
        self.city = city
        self.organisation = organisation


def getParticipantsSorted(url):
    df = pd.read_csv(url)
    participant_list = []
    for i in range(len(df)):
        person = Person(name=df["Имя"][i],
                        surname=df["Фамилия"][i],
                        patronymic=df["Отчество"][i],
                        city=df["Город"][i],
                        organisation=df["Организация"][i]
                        )
        participant_list.append(person)

    participant_list = sorted(
        participant_list, key=lambda p: p.surname + p.name + p.patronymic)
    return participant_list


def updateList(path="./content/2023/list.md"):
    partipants = getParticipantsSorted(url)

    with open(path, "w") as f:
        print(
            f'+++\ntitle = "Зарегистрированные участники"\n+++\n', file=f)
        print("<table>", file=f)
        for i in range(len(partipants)):
            p = partipants[i]
            full_name = f"{p.surname} {p.name} {p.patronymic}".replace(
                "-", "").strip()
            print(
                f"<tr><td>{i+1}</td><td>{full_name}</td><td>{p.city}</td><td>{p.organisation}</td></tr>",
                file=f)
        print("</table>", file=f)


updateList()
