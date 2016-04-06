var ListSearchedCars = React.createClass({

    getInitialState: function() {
    return{
        listofcars: [],
        car_search: ''
    };
  },

    /*componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/listsearchedcars',
            data: '',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});

  },*/

    changepage: function (result) {
        this.setState({
                listofcars: result.data
        });
    },

    handleSubmit: function (e){
        e.preventDefault()
        console.log('cheguei aqui')

        var data ={
            car_search: this.state.car_search
        }

        $.ajax({
            type: "POST",
            url: '/listsearchedcars',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});
    },

        car_searchChange: function (e) {
        this.setState({car_search: e.target.value})
    },

    render: function() {
        var createItem = function(item) {
            var linha = [<td>
                    <a href={'cardetail?id='+item.id}>{item.brand}</a></td>,
                            <td>{item.model}</td>,<td>{item.fuel}</td>,<td>{item.price}€</td>]
            return (<tr>{linha}</tr>)
        };

        return (
            <div id="teste">
                <form onSubmit={this.handleSubmit}>
                    <table>
                        <tr>
                            <td>Search Keywords</td>
                            <td>Brand</td>
                            <td>Model</td>
                            <td>Fuel</td>
                            <td>Price Range</td>
                            <td>Kilometer Range</td>
                        </tr>
                        <tr>
                            <td><input type="text" name="keyword"/></td>
                            <td><select>
                                <option selected="selected">All</option>
                                <option>Audi</option>
                                <option>BMW</option>
                                <option>Mercedes</option>
                                <option>Opel</option>
                                <option>Wolkswagen</option>
                            </select></td>
                            <td><select>
                                <option selected="selected">All</option>
                            </select></td>
                            <td><select>
                                <option selected="selected">All</option>
                                <option>Gasoline</option>
                                <option>Diesel</option>
                            </select></td>
                            <td><select>
                                <option selected="selected">All Prices</option>
                                <option>0€ - 5.000€</option>
                                <option>5.000€ - 10.000€</option>
                                <option>10.000€ - 15.000€</option>
                                <option>15.000€ - 20.000€</option>
                                <option>20.000€ - 25.000€</option>
                                <option>25.000€ - 30.000€</option>
                            </select></td>
                            <td><select>
                                <option selected="selected">All</option>
                                <option>My District</option>
                                <option>30KM - 40KM</option>
                                <option>40KM - 50KM</option>
                                <option>50KM - 60KM</option>
                                <option>60KM - 70KM</option>
                                <option>70KM - 80KM</option>
                            </select></td>
                            <td><input type="submit" value="Submit"/></td>
                        </tr>
                    </table>
                </form>
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
            </div>
      )
    }
});

ReactDOM.render(<ListSearchedCars />, list_searchedcars);
