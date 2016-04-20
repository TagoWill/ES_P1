
var ListClients = React.createClass({

    getInitialState: function() {
    return{
        listofusers: [],
        so_search: ''
    };
  },

    componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/listclients',
            data: '',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});

  },

    changepage: function (result) {
        this.setState({
                listofusers: result.data
        });
    },

    handleSubmit: function (e){
        e.preventDefault()
        console.log('cheguei aqui')

        var data ={
            so_search: this.state.so_search
        }

        $.ajax({
            type: "POST",
            url: '/listclients',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});
    },

        so_searchChange: function (e) {
        this.setState({so_search: e.target.value})
    },

    render: function() {
        var createItem = function(item) {
            var linha = [<td>{item.name}</td>,<td>{item.email}</td>,<td>{item.district}</td>]
            return (<tr>{linha}</tr>)
        };

        return (
            <form onSubmit={this.handleSubmit}>
                <input type="text" placeholder="Type name here" onChange={this.so_searchChange} value={this.state.so_search}/>
                <br></br><br></br>
                <input type="submit" name="search" value="Search"/>
                <br></br><br></br>
                <table>
                    <thead>
                        <tr>
                            <td><b>Name</b></td>
                            <td><b>Email</b></td>
                            <td><b>District</b></td>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.listofusers.map(createItem)}
                    </tbody>
                </table>
            </form>
      )
    }
});

ReactDOM.render(<ListClients />, list_clients);