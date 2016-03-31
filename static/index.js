var Index = React.createClass({

    getInitialState: function() {
    return{
        email: '',
        pass: ''
    };
  },

    handleSubmit: function (e){
        e.preventDefault()
        console.log('cheguei aqui')

        var data = {
            email: this.state.email,
            pass: this.state.pass
        }

        console.log(data)

        $.ajax({
            type: "POST",
            url: '/',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            //error: this.handleSubmitFailure,
            dataType: 'json',
            success: this.changepage
		});

    },

    changepage: function (result) {
        console.log(result);
    },
    
    emailChange: function (e) {
        this.setState({email: e.target.value})
    },

    passChange: function (e) {
        this.setState({pass: e.target.value})
    },
    
    render: function() {
        return (
        <form onSubmit={this.handleSubmit}>
            Email: <input type="text" onChange={this.emailChange} value={ this.state.email}/><br/>
            Password: <input type="text" onChange={this.passChange} value={ this.state.pass}/><br/>
          <button type="submit">Submit</button>
        </form>
      )
    }
});

ReactDOM.render(<Index />, login);