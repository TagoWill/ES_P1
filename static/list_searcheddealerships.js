var SearchDealerships = React.createClass({

    getInitialState: function() {
    return{
        listofdeals: [],
        orientation: 'DES',
        so_search: ''
    };
  },

    componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/listsearcheddealerships',
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

    so_searchChange: function (e) {
        this.setState({so_search: e.target.value})
    },

    handleSubmit: function (e){
        e.preventDefault()
        //console.log('cheguei aqui')

        if(this.state.orientation == 'ASC'){
            this.setState({orientation: 'DES'});
        }else{
            this.setState({orientation: 'ASC'});
        }

        var data ={
            so_search: this.state.so_search,
            orientation: this.state.orientation
        };

        $.ajax({
            type: "POST",
            url: '/listsearcheddealerships',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});
    },

    handleSubmit2: function (e){
        e.preventDefault()
        //console.log('cheguei aqui')

        var data ={
            so_search: this.state.so_search,
            orientation: this.state.orientation
        }

        $.ajax({
            type: "POST",
            url: '/listsearcheddealerships',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});
    },

    render: function() {
        var createItem = function(item) {
            var linha = [<td><a href={'dealershipdetails?id='+item.id}>{item.name}</a></td>,
                <td>{item.contact}</td>,<td>{item.district}</td>]
            return (<tr>{linha}</tr>)
        };

        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <input type="submit" value="Sort by Name"/>
                    <br></br><br></br>
                </form>
                <form onSubmit={this.handleSubmit2}>
                    <input type="text" placeholder="Type name here" onChange={this.so_searchChange} value={this.state.so_search}/>
                    <br></br><br></br>
                    <input type="submit" name="search" value="Search"/>
                    <br></br><br></br>
                    <table>
                        <thead>
                        <tr>
                            <td>Name</td>
                            <td>Contact</td>
                            <td>District</td>
                        </tr>
                        </thead>
                        <tbody>
                            {this.state.listofdeals.map(createItem)}
                        </tbody>
                    </table>
                </form>
            </div>
      )
    }
});

ReactDOM.render(<SearchDealerships />, searchdealerships);

