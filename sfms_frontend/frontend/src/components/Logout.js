const Logout = () => {

    var axios = require('axios');
   
    var config = {
    method: 'get',
    url: '/api/v1/logout',

    };

    axios(config)
    .then(function (response) {
    console.log(JSON.stringify(response.data));
    window.location.replace('http://localhost:3000/');
    })
    .catch(function (error) {
    console.log(error);
    });

}
export default Logout