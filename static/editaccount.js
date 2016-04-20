var EditAccount = React.createClass({

    getInitialState: function() {
    return{
        name: '',
        email: '',
        district: '',
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
        //console.log('handleSubmit')

        var data = {
            name: this.state.name,
            email: this.state.email,
            district: this.state.district,
            password: this.state.password
        }

        //console.log(data)

        if (data.password!=undefined) {
            $.ajax({
                type: "POST",
                url: '/editaccount',
                data: JSON.stringify(data),
                contentType: 'application/json;charset=UTF-8',
                //error: this.handleSubmitFailure,
                dataType: 'json',
                success: this.changepage
		    })
            ReactDOM.render(<AccountSUCCESSMsg/>, accountactionmsg);
        }
        else {
            //console.log(data);
            ReactDOM.render(<AccountERRORMsg/>, accountactionmsg);
        }
    },
    
    handleDeleteSubmit: function (){
        console.log("handleDeleteSubmit"+this.state.name+this.state.email);
        var data = {
            name: this.state.name,
            email: this.state.email
        }

        //console.log("data: "+data)

        $.ajax({
            type: "POST",
            url: '/deleteaccount',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            //error: this.handleSubmitFailure,
            dataType: 'json'
            //success: this.changepage
		});
        ReactDOM.render(<AccountDELETEDMsg/>, accountactionmsg);
    },

    changepage: function (result) {
        //console.log(result);
        //console.log(result.name);
        this.setState({name: result.name})
        this.setState({email: result.email})
        this.setState({district: result.district})
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
    
    districtChange: function (e) {
        this.setState({district: e.target.district})
    },

    PopUpFunction: function () {
        if (confirm("Are you sure?") == true) {
            //console.log("myfunction");
            this.handleDeleteSubmit()
        }
    },

    render: function() {
        return (
            <div id="editaccount_div">
                <form onSubmit={this.handleSubmit}>
                    <br></br>
                    Name: <input type="text" onChange={this.nameChange} value={this.state.name}/>
                    <br></br>
                    <br></br>
                    Email: <input type="text" onChange={this.emailChange} value={this.state.email}/>
                    <br></br>
                    <br></br>
                    District: <input type="text" onChange={this.districtChange} value={this.state.district}/>
                    <br></br>
                    <br></br>
                    Password: <input type="password" onChange={this.passChange} value={this.state.password}/>
                    <br></br>
                    <br></br>
                    <input type="submit" value="Save Changes"/>
                </form>
                <br></br>
                <br></br>
                <button onClick={this.PopUpFunction}>Delete Account</button>
            </div>
        )
    }
});

var AccountERRORMsg = React.createClass({
    render: function() {
        return (
            <div id="accountactionmsg_div">
                Error: Password must be submited in order to edit!
            </div>
        )
    }
});

var AccountSUCCESSMsg = React.createClass({
    render: function() {
        return (
            <div id="accountactionmsg_div">
                Account Successfully Edited!
            </div>
        )
    }
});

var AccountDELETEDMsg = React.createClass({
    render: function() {
        return (
            <div id="accountactionmsg_div">
                Account Successfully Deleted!
            </div>
        )
    }
});

ReactDOM.render(<EditAccount />, editaccount);