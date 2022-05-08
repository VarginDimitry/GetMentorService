import {useState} from "react";

function App() {
    let [time, setTime] = useState(0)
    // let email = "var2qaik.boom@gmail.com";
    // let password = "qwe321";
    const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTgwMzI1NjMsImlhdCI6MTY1MjAzMjU2MywiaWQiOiIzNzg1NjQxNS0zNmMxLTQwMDAtOTlmNS0wODU1MDY0MWJkYWUiLCJlbWFpbCI6ImRpbWEzQGdtYWlsLmNvbSJ9.oDp-Q_FV_3DrgsgrNhpdpb-y7DeTtk_jVmhBX6uTLlw'
  const update_me = () => {
      fetch("/api/v1/user/update_me", {
          method: "POST",
        headers: {
          'Content-Type': 'application/json',
            'Authorization': token,
        },
          body: JSON.stringify({
                "first_name": "Dmitry",
                "last_name": "Suchek"
            })
      }).then((response) => {
          response.json().then((body) => {
              console.log(body)
          })
      })
  }
  update_me();
  // const get_time = () => {
  //     fetch("/time", {
  //         method: "GET",
  //     }).then((response) => {
  //         response.json().then((body) => {
  //             setTime(body['time'])
  //         })
  //     })
  // }
  // get_time()

  return (
    <div className="App">
      <h1>{time}</h1>
    </div>
  );
}

export default App;
