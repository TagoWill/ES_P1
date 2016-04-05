
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

        var linha = [<td><b>name</b></td>,<td><b>email</b></td>]
        var createItem = function(item) {
            var linha = [<td>
                    <a href={'clientdetail?email='+item.email}>{item.name}</a></td>,<td>{item.email}</td>]
            return (<tr>{linha}</tr>)
        };

        return (
            <form onSubmit={this.handleSubmit}>
            <table>
                <thead>
                <tr>
                    <th>Client</th>
                </tr>
                <tr>
                    <td><input type="text" onChange={this.so_searchChange} value={ this.state.so_search}/></td>
                    <td><input type="submit" name="search"/></td>
                </tr>
                    <tr>
                        {linha}
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