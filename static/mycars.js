var MyCars = React.createClass({

    getInitialState: function() {
    return{
        listofcars: [],
        dl_search: ''
    };
  },

    componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/listmycars',
            data: '',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});

  },

    changepage: function (result) {
        this.setState({
                listofcars: result.data
        });
    },

    handleSubmit: function (e){
        e.preventDefault()
        console.log('cheguei aqui')

        var data ={
            dl_search: this.state.dl_search
        }

        $.ajax({
            type: "POST",
            url: '/listmycars',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});
    },

    render: function() {
        var createItem = function(item) {
            var linha = [<td>
                    <a href={'cardetail?id='+item.id}>{item.brand}</a></td>,
                            <td>{item.model}</td>,<td>{item.fuel}</td>,<td>{item.price}€</td>]
            return (<tr>{linha}</tr>)
        };

        return (
            <form onSubmit={this.handleSubmit}>
            <table>
                <thead>
                <tr>
                    <th>Brand</th>
                    <th>Model</th>
                    <th>Fuel</th>
                    <th>Price</th>
                </tr>
                </thead>
                <tbody>
                    {this.state.listofcars.map(createItem)}
                </tbody>
            </table>
            </form>
      )
    }
});

ReactDOM.render(<MyCars />, list_mycars);