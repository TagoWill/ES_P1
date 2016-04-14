var ListSearchedCars = React.createClass({

    getInitialState: function() {
    return{
        listofcars: [],
        car_search_brand: 'All',
        car_search_model: 'All',
        car_search_fuel: 'All',
        car_search_price: 'All Prices',
        car_search_kmrange: 'All'
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
            car_search_price: this.state.car_search_price,
            car_search_kmrange: this.state.car_search_kmrange
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
        //IR A BASE DE DADOS BUSCAR MODELOS
        //MODIFICAR VARIAVEL COM NOVOS MODELOS.
        //FAZER RENDER
        ReactDOM.render(<ModelSelectBox/>, modelselect);
    },

    car_searchChange_model: function (e) {
        this.setState({car_search_model: e.target.value})
    },

    car_searchChange_fuel: function (e) {
        this.setState({car_search_fuel: e.target.value})
    },

    car_searchChange_price: function (e) {
        this.setState({car_search_price: e.target.value})
    },

    car_searchChange_kmrange: function (e) {
        this.setState({car_search_kmrange: e.target.value})
    },

    render: function() {
        var createItem = function(item) {
            var linha = [<td>
                    <a href={'cardetail?id='+item.id}>{item.brand}</a></td>,,<td>{item.model}</td>,
                            <td>{item.fuel}</td>,<td>{item.price}€</td>,<td>{item.dealership}</td>,<td>{item.district}</td>]
            return (<tr>{linha}</tr>)
        };

        return (
            <div id="search_div">
                <form onSubmit={this.handleSubmit}>
                    <table>
                        <tr>
                            <td>Brand</td>
                            <td>Model</td>
                            <td>Fuel</td>
                            <td>Price Range (€)</td>
                            <td>Kilometer Range</td>
                        </tr>
                        <tr>
                            <td><select onChange={this.car_searchChange_brand} value={this.state.car_search_brand}>
                                <option defaultValue="selected">All</option>
                                <option>Audi</option>
                                <option>BMW</option>
                                <option>Ferrari</option>
                                <option>Fiat</option>
                                <option>Mercedes</option>
                                <option>Opel</option>
                                <option>Seat</option>
                                <option>Wolkswagen</option>
                            </select></td>
                            <td><select onChange={this.car_searchChange_model} value={this.state.car_search_model}>
                                <option defaultValue="selected">All</option>
                                <option>320i</option>
                                <option>SLK200</option>
                                <!-- FAZER ISTO DINAMICO -->
                                <!-- {this.state.variavel.map(funcao)} -->
                            </select></td>
                            <td><select onChange={this.car_searchChange_fuel} value={this.state.car_search_fuel}>
                                <option defaultValue="selected">All</option>
                                <option>Gasoline</option>
                                <option>Diesel</option>
                            </select></td>
                            <td><select onChange={this.car_searchChange_price} value={this.state.car_search_price}>
                                <option defaultValue="selected">All Prices</option>
                                <option>0 - 5.000</option>
                                <option>5.000 - 10.000</option>
                                <option>10.000 - 15.000</option>
                                <option>15.000 - 20.000</option>
                                <option>20.000 - 25.000</option>
                                <option>25.000 - 30.000</option>
                                <option>>=30.000</option>
                            </select></td>
                            <td><select onChange={this.car_searchChange_kmrange} value={this.state.car_search_kmrange}>
                                <option defaultValue="selected">All</option>
                                <option>Coimbra</option>
                                <option>30KM - 40KM</option>
                                <option>40KM - 50KM</option>
                                <option>50KM - 60KM</option>
                                <option>60KM - 70KM</option>
                                <option>70KM - 80KM</option>
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

var ModelSelectBox = React.createClass({
    render: function() {
        return (
            <div id="modelselect_div">
                <select>
                    <option defaultValue="selected">All</option>
                    <option>320i</option>
                    <option>SLK200</option>
                </select>
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
