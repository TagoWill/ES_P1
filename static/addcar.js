var AddCar = React.createClass({

    getInitialState: function() {
    return{
        brand: '',
        model: '',
        fuel: '',
        price: '',
        kms: '',
        year: ''
    };
  },

    componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/add_car',
            data: '',
            contentType: 'application/json;charset=UTF-8',
            //error: this.handleSubmitFailure,
            success: this.changepage
		});

  },


    handleSubmit: function (e){
        e.preventDefault()

        var data = {
            brand: this.state.brand,
            model: this.state.model,
            fuel: this.state.fuel,
            price: this.state.price,
            kms: this.state.kms,
            year: this.state.year
        }

        console.log(data)

        $.ajax({
            type: "POST",
            url: '/add_car',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            //error: this.handleSubmitFailure,
            dataType: 'json',
            success: this.changepage
		});
    },

    changepage: function (result) {
        console.log(result);
        console.log(result.brand);
        this.setState({brand: result.brand})
        this.setState({model: result.model})
        this.setState({fuel: result.fuel})
        this.setState({price: result.price})
        this.setState({kms: result.kms})
        this.setState({year: result.year})
    },

    modelChange: function (e) {
        this.setState({model: e.target.value})
    },

    priceChange: function (e) {
        this.setState({price: e.target.value})
    },

    fuelChange: function (e) {
        this.setState({fuel: e.target.value})
    },

    brandChange: function (e) {
        this.setState({brand: e.target.value})
    },
    
    kmsChange: function (e) {
        this.setState({kms: e.target.value})
    },
    
    yearChange: function (e) {
        this.setState({year: e.target.value})
    },

    render: function() {
        return (
            <form onSubmit={this.handleSubmit}>
                <br></br>
                Brand: <input type="text" onChange={this.brandChange} value={ this.state.brand}/>
                <br></br>
                <br></br>
                Model: <input type="text" onChange={this.modelChange} value={ this.state.model}/>
                <br></br>
                <br></br>
                Fuel: <input type="text" onChange={this.fuelChange} value={ this.state.fuel}/>
                <br></br>
                <br></br>
                Price: <input type="text" onChange={this.priceChange} value={ this.state.price}/>
                <br></br>
                <br></br>
                Kms: <input type="text" onChange={this.kmsChange} value={ this.state.kms}/>
                <br></br>
                <br></br>
                Year: <input type="text" onChange={this.yearChange} value={ this.state.year}/>
                <br></br>
                <br></br>
                <input type="submit" value="Save"/>
            </form>
      )
    }
});

ReactDOM.render(<AddCar />, addcar);
