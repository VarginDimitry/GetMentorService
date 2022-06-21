import asyncio
import random
import string

import aiohttp

BASE_URL = 'http://51.250.102.238'
API = f"{BASE_URL}/api/v1"

man_first_names = ["Dmitry", "Michail", "Sergei", "Anton", "Alexander"]
man_last_names = ["Vargin", "Ivanov", "Votinov", "Testovii", "Pavlov"]
woman_first_names = ["Ksenia", "Anastasia", "Irina", "Kate", "Evgenia"]
woman_last_names = ["Votinova", "Vargina", "Kulagina", "Pavlova", "Testovaya"]
job = ["Google", "Yandex", "Apple", "Epam", "Huawei"]
skill_grade = ['good', 'bad', 'average']
# ['backend', 'frontend', 'android', 'ios', 'devops', 'design']
skills = [
    {'category': 'backend', 'name': 'Python'},
    {'category': 'backend', 'name': 'GoLang'},
    {'category': 'backend', 'name': 'Java'},

    {'category': 'frontend', 'name': 'JS'},
    {'category': 'frontend', 'name': 'TS'},

    {'category': 'android', 'name': 'Java'},
    {'category': 'android', 'name': 'Kotlin'},

    {'category': 'ios', 'name': 'Swift'},
    {'category': 'ios', 'name': 'Objective-C'},

    {'category': 'devops', 'name': 'Docker'},
    {'category': 'devops', 'name': 'Kubernetes'},

    {'category': 'design', 'name': 'Figma'},
    {'category': 'design', 'name': 'Adobe Photoshop'},

]


# price string "1000$"
# price string "1000$"
# expirience string "10 years"
# about string

async def main():
    async with aiohttp.ClientSession() as session:
        for skill in skills:
            # registration
            is_man = bool(random.randint(0, 1))
            first_name = random.choice(man_first_names if is_man else woman_first_names)
            last_name = random.choice(man_last_names if is_man else woman_last_names)
            password = "".join(random.choices(string.ascii_letters, k=16))
            email = f"{first_name.lower()}{random.randint(0, 100_000)}@yandex.ru"
            doc = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password
            }
            async with session.post(f"{API}/auth/registration", json=doc) as resp:
                assert int(resp.status) == 200, await resp.json()
                # login
                headers = {'Authorization': None}
                doc = {
                    "email": email,
                    "password": password
                }
                async with session.post(f"{API}/auth/login", json=doc) as resp:
                    assert int(resp.status) == 200, await resp.json()
                    headers['Authorization'] = (await resp.json())['accessToken']
                    doc = {
                        "category": skill['category'],
                        "job": random.choice(job),
                        "price": f"{random.randint(10, 1000)}$",
                        "experience": f"{random.randint(1, 15)} years",
                        "about": "ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА | ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА |ЗДЕСЬ МОГЛАБЫТЬ ВАША РЕКЛАМА",
                        "skills": [
                            {
                                "grade": random.choice(skill_grade),
                            } | skill
                        ]
                    }
                    async with session.post(f"{API}/cv/create_cv", json=doc, headers=headers) as resp:
                        assert int(resp.status) == 200, await resp.json()


if __name__ == '__main__':
    asyncio.run(main())
