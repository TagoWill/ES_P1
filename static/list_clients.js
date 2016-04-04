var ListClients = React.createClass({

    getInitialState: function() {
    return{
        listofusers: []
    };
  },

    componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/search_clients',
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

    render: function() {

        var createItem = function(item) {
            return <li><a href={'clientdetail?email='+item.email}>{item.name} - {item.email}</a></li>;
        };

        return (
            <ul>
                {this.state.listofusers.map(createItem)}
            </ul>
      )
    }
});

ReactDOM.render(<ListClients />, list_clients);