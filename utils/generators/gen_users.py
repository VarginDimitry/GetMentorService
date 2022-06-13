import random
import requests as requests

local_host = 'http://localhost:5000'

host = local_host

skills = [
    {
        "grade": 10,
        "name": "Python4",
        "category": "Programming"
    },
    {
        "grade": 5,
        "name": "Java4",
        "category": "Programming"
    },
    {
        "grade": 1,
        "name": "English",
        "category": "Language"
    },
    {
        "grade": 5,
        "name": "Docker",
        "category": "Devops"
    },
    {
        "grade": 5,
        "name": "GOTOvit pelmeni",
        "category": "Cooking"
    }
]


def gen_users_with_cvs(user_num: int, cvs_per_user: int) -> None:
    with requests.Session() as s:
        for i in range(1, user_num + 1):
            print(i)
            email = f'user{i}@gmail.com'
            password = 'qwe323'
            reg_res = s.post(
                url=host + '/api/v1/auth/registration',
                json={
                    "first_name": "Dmitry",
                    "last_name": "Vargin",
                    "gender": "M",

                    "email": email,
                    "password": password,

                    "phone": "+79960653096",
                    "telegram_profile": "@dmitry_vargin",
                    "middle_name": "Alexandrovich"
                }
            )
            assert reg_res.status_code == 200, reg_res.json()
            login_res = s.get(
                url=host + "/api/v1/auth/login",
                json={
                    'email': email,
                    'password': password,
                }
            )
            assert login_res.status_code == 200, reg_res.json()
            s.headers = {'Authorization': login_res.json()['accessToken']}

            for j in range(cvs_per_user):
                create_cv_res = s.post(
                    url=host + "/api/v1/cv/create_cv",
                    json={"skills": list(random.sample(skills, k=random.randint(0, len(skills))))}
                )
                assert create_cv_res.status_code == 200, reg_res.json()

            s.headers = {}


if __name__ == '__main__':
    gen_users_with_cvs(10, 1)
