var MyDealerships = React.createClass({

    getInitialState: function() {
    return{
        listofdeals: [],
        orientation: 'DES'
    };
  },

    componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/listmydealerships',
            data: '',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});

  },

    changepage: function (result) {
        this.setState({
                listofdeals: result.data
        });
    },

    handleSubmit: function (e){
        e.preventDefault()
        console.log('cheguei aqui')

        if(this.state.orientation == 'ASC'){
            this.setState({orientation: 'DES'});
        }else{
            this.setState({orientation: 'ASC'});
        }

        var data ={
            orientation: this.state.orientation
        };

        $.ajax({
            type: "POST",
            url: '/listmydealerships',
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
                    <a href={'mydealershipdetails?id='+item.id}>{item.name}</a></td>,
                                    <td>{item.contact}</td>,<td>{item.district}</td>, <td><a href={'editdealership?id='+item.id}>click</a></td>]
            return (<tr>{linha}</tr>)
        };

        return (
            <form onSubmit={this.handleSubmit}>
                <button type="submit">Sort</button>
            <table>
                <thead>
                <tr>
                    <th>Name</th>
                    <th>Contact</th>
                    <th>District</th>
                    <th>Edit</th>
                </tr>
                </thead>
                <tbody>
                    {this.state.listofdeals.map(createItem)}
                </tbody>
            </table>

            </form>
      )
    }
});

ReactDOM.render(<MyDealerships />, list_mydealerships);
