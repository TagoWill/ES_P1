var MyCars = React.createClass({

    getInitialState: function() {
    return{
        listofcars: [],
        listofdealeships: [],
        dl_search: '',
        selectedcar: '1',
        selecteddealership: '1',
        sort_by: 'Sort by Brand (A-Z)'
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

        $.ajax({
            type: "GET",
            url: '/listmydealerships',
            data: '',
            //error: this.handleSubmitFailure,
            success: this.changeDealership
		});
  },

    changeDealership: function (result) {
        /*console.log(result.data);*/
        this.setState({
            listofdealeships: result.data
        });
        /*console.log(this.state.listofdealeships);*/
    },

    changepage: function (result) {
        this.setState({
                listofcars: result.data
        });
    },

    change_sort_by: function (e) {
        this.setState({
                sort_by: e.target.value
        });
    },
    
    handleSubmit: function (e){
        e.preventDefault()
        //console.log('cheguei aqui')

        var data ={
            sort_by: this.state.sort_by
        };

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

    createlistcars: function (item) {
        var linha = [
            <td><img src={"https://s3-eu-west-1.amazonaws.com/esimages3bucket/"+item.id + ".jpg"} alt="Imagem em falta" height="100" width="120"/></td>,
            <td>{item.brand}</td>,
            <td>{item.model}</td>,
            <td>{item.fuel}</td>,
            <td>{item.price}€</td>,
            <td>{item.kms}</td>,
            <td>{item.year}</td>,
            <td><a href={'editcar?id='+item.id}>click</a></td>,
            <td><a href={'delete_car?id='+item.id}>click</a></td>]
            return (<tr>{linha}</tr>)
    },

    render: function() {
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <select onChange={this.change_sort_by} value={this.state.sort_by}>
                        <option>Sort by Brand (A-Z)</option>
                        <option>Sort by Brand (Z-A)</option>
                        <option>Sort by Brand and Model (A-Z)</option>
                        <option>Sort by Brand and Model (Z-A)</option>
                        <option>Sort by Price (Ascending)</option>
                        <option>Sort by Price (Descending)</option>
                    </select>
                    <input type="submit" value="Sort Cars"/>
                </form>
                <br></br><br></br>
                <table>
                    <thead>
                    <tr>
                        <td>Image</td>
                        <td>Brand</td>
                        <td>Model</td>
                        <td>Fuel</td>
                        <td>Price</td>
                        <td>Kms</td>
                        <td>Year</td>
                        <td>Edit</td>
                        <td>Delete</td>
                    </tr>
                    </thead>
                    <tbody>
                        {this.state.listofcars.map(this.createlistcars)}
                    </tbody>
                </table>
            </div>
      )
    }
});

ReactDOM.render(<MyCars />, list_mycars);