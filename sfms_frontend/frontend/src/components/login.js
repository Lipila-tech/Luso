import React from 'react';  
import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
import SelectTableComponent from "../pages/selectTableComponent";
import Alert from 'react-popup-alert'
import '../styles.scss';

const App = () => {  
  const [alert, setAlert] = React.useState({
    type: 'error',
    text: 'This is a alert message',
    show: false
  })

  function onCloseAlert() {
    setAlert({
      type: '',
      text: '',
      show: false
    })
  }

  function onShowAlert(type) {
    setAlert({
      type: type,
      text: 'Pay k8000',
      show: true
    })
  }
  
    return (  
          <div className='container-lg'>  
            <h2 className='d-flex justify-content-center'>Select Items to Pay for</h2>
            <br/>
              <SelectTableComponent />
              <br/>
                <p >Enter Total amount to pay:
                  <input name="amount" type="number" placeholder='amount'></input></p> 
                <p >Enter Mobile number to use:
                  <input name="mobile" type="number" placeholder='0969620939'></input></p>
                <br/>
                <div style={{ display: 'flex', justifyContent: 'center', marginTop: 50 }}>
                  <button onClick={() => onShowAlert('info')}>Confirm</button>
              </div>    
          <Alert
        header={'Confirm Payment'}
        btnText={'Close'}
        text={alert.text}
        type={alert.type}
        show={alert.show}
        onClosePress={onCloseAlert}
        pressCloseOnOutsideClick={true}
        showBorderBottom={true}
        alertStyles={{}}
        headerStyles={{}}
        textStyles={{}}
        buttonStyles={{}}
      />  
          </div>  
    )
  }  

  export default App