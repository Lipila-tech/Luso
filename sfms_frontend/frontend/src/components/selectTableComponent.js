import React from "react";

const history = [
    {
        id: 1,
        selected: false,
        term: "Two 2022",
        paid: 3000,
        pending: 1000,
        amount_to_pay: 1000,
    },
];

class SelectTableComponent extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            List: history,
            MasterChecked: false,
            SelectedList: [],
        };
    }

// select or unselect table rows
onMasterCheck(e) {
    let tempList = this.state.List;
    // check/ unckeck all items
    tempList.map((user) => (user.selected = e.target.checked));

    //update state
    this.setState({
        MasterChecked: e.target.checked,
        List: tempList,
        SelectedList: this.state.List.filter((e) => e.selected),
    });
}

//update List items state and Master Checkbox State
onItemCheck(e, item) {
    let tempList = this.state.List;
    tempList.map((user) => {
        if (user.id === item.id) {
            user.selected = e.target.checked;
        }
        return user;
    });

    // To control master checkbox state
    const totalItems = this.state.List.length;
    const totalCheckedItems = tempList.filter((e) => e.selected).length;

    // Update state
    this.setState({
        MasterChecked: totalItems === totalCheckedItems,
        List: tempList,
        SelectedList: this.state.List.filter((e) => e.selected),
    });
}

// Event to get selected rows(optional)
getSelectedRows() {
    this.setState({
        SelectedList: this.state.List.filter((e) => e.selected),
    });
}

render () {

    return (

        <div className="container">
        <div className="row">
          <div className="col-md-12">
            <table className="table">
              <thead>
                <tr>
                  <th scope="col">
                    <input
                      type="checkbox"
                      className="form-check-input"
                      checked={this.state.MasterChecked}
                      id="mastercheck"
                      onChange={(e) => this.onMasterCheck(e)}
                    />
                  </th>
                  <th scope="col">Term</th>
                  <th scope="col">Paid</th>
                  <th scope="col">Pending</th>
                  <th scope="col">Amount to Pay</th>
                </tr>
              </thead>
              <tbody>
                {this.state.List.map((user) => (
                  <tr key={user.id} className={user.selected ? "selected" : ""}>
                    <th scope="row">
                      <input
                        type="checkbox"
                        checked={user.selected}
                        className="form-check-input"
                        id="rowcheck{user.id}"
                        onChange={(e) => this.onItemCheck(e, user)}
                      />
                    </th>
                    <td>{user.term}</td>
                    <td>{user.paid}</td>
                    <td>{user.pending}</td>
                    <td>{user.amount_to_pay}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {/* <h3
              className="btn btn-primary"
            >
              Number of Selected Items {this.state.SelectedList.length} 
            </h3>
            <div className="row">
              <b>Selected Row Items:</b>
              <code>{JSON.stringify(this.state.SelectedList)}</code>
            </div> */}
          </div>
        </div>
      </div>
    );
  }
}
export default SelectTableComponent;