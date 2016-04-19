var ListSearchedCars = React.createClass({

    getInitialState: function() {
    return{
        listofcars: [],
        car_search_brand: 'All',
        car_search_model: 'All',
        car_search_fuel: 'All',
        car_search_minprice: '0',
        car_search_maxprice: '50000',
        car_search_kmrange: 'All',
        car_search_year: 'All',
        list_of_models: []
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
        //console.log("result: "+result.data);
        this.setState({
            listofcars: result.data
        });
        if (result.data!='') {
            ReactDOM.render(<CarsFOUNDMsg/>, actionmsg);
        } else {
            ReactDOM.render(<CarsNOTFOUNDMsg/>, actionmsg);
        }
    },

    handleSubmit: function (e){
        e.preventDefault()
        //console.log('cheguei aqui')

        var data ={
            car_search_brand: this.state.car_search_brand,
            car_search_model: this.state.car_search_model,
            car_search_fuel: this.state.car_search_fuel,
            car_search_minprice: this.state.car_search_minprice,
            car_search_maxprice: this.state.car_search_maxprice,
            car_search_kmrange: this.state.car_search_kmrange,
            car_search_year: this.state.car_search_year
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

    car_searchChange_brand: function (e) {
        this.setState({car_search_brand: e.target.value});

        var data = {
            car_search_brand: e.target.value
        }

        $.ajax({
            type: "POST",
            url: '/getmodels',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            //error: this.handleSubmitFailure,
            success: this.handleListOfModels
		});
    },

    handleListOfModels:function (result) {
        //console.log(result.data)
        this.setState({list_of_models: result.data});
    },

    car_searchChange_model: function (e) {
        this.setState({car_search_model: e.target.value})
    },

    car_searchChange_fuel: function (e) {
        this.setState({car_search_fuel: e.target.value})
    },

    car_searchChange_minprice: function (e) {
        this.setState({car_search_minprice: e.target.value})
    },

    car_searchChange_maxprice: function (e) {
        this.setState({car_search_maxprice: e.target.value})
    },

    car_searchChange_kmrange: function (e) {
        this.setState({car_search_kmrange: e.target.value})
    },

    render: function() {
        var createItem = function(item) {
            var linha = [<td>
                    <a href={'cardetail?id='+item.id}>{item.brand}</a></td>,<td>{item.model}</td>,
                            <td>{item.fuel}</td>,<td>{item.price}€</td>,<td>{item.kms}Kms</td>,<td>{item.year}</td>,
                            <td>{item.dealership}</td>,<td>{item.district}</td>];
            return (<tr>{linha}</tr>)
        };

        var iteracaoDosModels = function (item) {
            return <option>{item.model}</option>
        }

        return (
            <div id="search_div">
                <form onSubmit={this.handleSubmit}>
                    <table>
                        <tr>
                            <td>Brand</td>
                            <td>Model</td>
                            <td>Fuel</td>
                            <td>Minimum Price (€)</td>
                            <td>Maximum Price (€)</td>
                            <td>Kilometers Range</td>
                        </tr>
                        <tr>
                            <td><select onChange={this.car_searchChange_brand} value={this.state.car_search_brand}>
                                <option>All</option>
                                <option>Audi</option>
                                <option>BMW</option>
                                <option>Ferrari</option>
                                <option>Ford</option>
                                <option>Mercedes</option>
                                <option>Opel</option>
                                <option>Seat</option>
                                <option>Volkswagen</option>
                            </select></td>
                            <td><select onChange={this.car_searchChange_model} value={this.state.car_search_model}>
                                <option defaultValue="selected">All</option>
                                {this.state.list_of_models.map(iteracaoDosModels)}
                            </select></td>
                            <td><select onChange={this.car_searchChange_fuel} value={this.state.car_search_fuel}>
                                <option defaultValue="selected">All</option>
                                <option>Gasoline</option>
                                <option>Diesel</option>
                            </select></td>
                            <td><select onChange={this.car_searchChange_minprice} value={this.state.car_search_minprice}>
                                <option defaultValue="selected">0</option>
                                <option>5000</option>
                                <option>10000</option>
                                <option>15000</option>
                                <option>20000</option>
                                <option>25000</option>
                                <option>30000</option>
                                <option>35000</option>
                                <option>40000</option>
                                <option>45000</option>
                            </select></td>
                            <td><select onChange={this.car_searchChange_maxprice} value={this.state.car_search_maxprice}>
                                <option defaultValue="selected">50000</option>
                                <option>45000</option>
                                <option>40000</option>
                                <option>35000</option>
                                <option>30000</option>
                                <option>25000</option>
                                <option>20000</option>
                                <option>15000</option>
                                <option>10000</option>
                                <option>5000</option>
                            </select></td>
                            <td><select onChange={this.car_searchChange_kmrange} value={this.state.car_search_kmrange}>
                                <option defaultValue="selected">All</option>
                                <option>{"<="}50.000</option>
                                <option>{"<="}100.000</option>
                                <option>{"<="}150.000</option>
                                <option>{"<="}200.000</option>
                                <option>{"<="}250.000</option>
                                <option>{"<="}300.000</option>
                                <option>>300.000</option>
                            </select></td>
                            <td><input type="submit" value="Search"/></td>
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
                            <th>Kilometers</th>
                            <th>Year</th>
                            <th>Dealership</th>
                            <th>District</th>
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

var CarsFOUNDMsg = React.createClass({
    render: function() {
        console.log(ListSearchedCars.listofcars);
        return (
            <div id="actionmsg_div">
                Cars Found!
            </div>
        )
    }
});

var CarsNOTFOUNDMsg = React.createClass({
    render: function() {
        return (
            <div id="actionmsg_div">
                Cars Not Found!
            </div>
        )
    }
});

ReactDOM.render(<ListSearchedCars />, list_searchedcars);
