import {useState} from "react";

function App() {
    let [time, setTime] = useState(0)
    let email = "var2qaik.boom@gmail.com";
    let password = "qwe321";
  const registration = () => {
      fetch("http://localhost:5000/api/v1/auth/registration", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
              "Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
              "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"
          },
          body: JSON.stringify({
            "first_name": "Dmitry",
            "last_name": "Vargin",
            "gender": "M",

            "email": email,
            "password": password,

            "phone": "+79960653096",
            "telegram_profile": "@dmitry_vargin",
            "middle_name": "Alexandrovich"
          })
      }).then((response) => {
          response.json().then((body) => {
              console.log("reg", body)
          })
      })
  }

  const login = () => {
      fetch("http://localhost:5000/api/v1/auth/login", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "email": email,
        "password": password
    })
      }).then((response) => {
          response.json().then((body) => {
              console.log("login", body)
          })
      })
  }

  registration()
    login()

  const get_cvs = () => {
      fetch("http://localhost:5000/api/v1/cv/search_cv", {
          method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
          body: JSON.stringify({
            "limit": 100,
            "offset": 0,
            "sort_by": {
                "row": "skill_num",
                "order": "DESC"
            },
            "filters": {
                "skill_num": {
                    "from": 5
                }
            }
        })
      }).then((response) => {
          response.json().then((body) => {
              console.log(body)
          })
      })
  }

  get_cvs();

  return (
    <div className="App">
      <h1>{time}</h1>
    </div>
  );
}

export default App;
