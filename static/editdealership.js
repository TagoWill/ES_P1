var EditDealership = React.createClass({

    getInitialState: function() {
    return{
        name: '',
        contact: '',
        district: ''
    };
  },

    componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/edit_dealership',
            data: '',
            contentType: 'application/json;charset=UTF-8',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});

  },


    handleSubmit: function (e){
        e.preventDefault()

        var data = {
            name: this.state.name,
            contact: this.state.contact,
            district: this.state.district
        }

        console.log(data)

        $.ajax({
            type: "POST",
            url: '/edit_dealership',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            //error: this.handleSubmitFailure,
            dataType: 'json',
            success: this.changepage
		});
    },

    changepage: function (result) {
        console.log(result);
        console.log(result.name);
        this.setState({name: result.name})
        this.setState({contact: result.contact})
        this.setState({district: result.district})
    },

    contactChange: function (e) {
        this.setState({contact: e.target.value})
    },

    districtChange: function (e) {
        this.setState({district: e.target.value})
    },

    nameChange: function (e) {
        this.setState({name: e.target.value})
    },

    render: function() {
        return (
            <form onSubmit={this.handleSubmit}>
                <br></br>
                Name: <input type="text" onChange={this.nameChange} value={ this.state.name}/>
                <br></br>
                <br></br>
                Contact: <input type="text" onChange={this.contactChange} value={ this.state.contact}/>
                <br></br>
                <br></br>
                District: <input type="text" onChange={this.districtChange} value={ this.state.district}/>
                <br></br>
                <br></br>
                <input type="submit" value="Save"/>
            </form>
      )
    }
});

ReactDOM.render(<EditDealership />, editdealership);
