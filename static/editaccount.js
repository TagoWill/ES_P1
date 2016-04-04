var EditAccount = React.createClass({

    getInitialState: function() {
    return{
        name: '',
        email: '',
        password: ''
    };
  },

    componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/editaccount',
            data: '',
            contentType: 'application/json;charset=UTF-8',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});

  },


    handleSubmit: function (e){
        e.preventDefault()
        console.log('cheguei aqui')

        var data = {
            name: this.state.name,
            email: this.state.email,
            password: this.state.password
        }

        console.log(data)

        $.ajax({
            type: "POST",
            url: '/editaccount',
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
        this.setState({email: result.email})
        this.setState({password: result.password})
    },

    emailChange: function (e) {
        this.setState({email: e.target.value})
    },

    passChange: function (e) {
        this.setState({password: e.target.value})
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
                Email: <input type="text" onChange={this.emailChange} value={ this.state.email}/>
                <br></br>
                <br></br>
                Password: <input type="password" onChange={this.passChange} value={ this.state.password}/>
                <br></br>
                <br></br>
                <input type="submit" value="Save"/>
            </form>
      )
    }
});

ReactDOM.render(<EditAccount />, editaccount);