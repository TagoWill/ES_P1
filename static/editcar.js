var AddCar = React.createClass({

    getInitialState: function() {
    return{
        brand: '',
        model: '',
        fuel: '',
        price: '',
        kms: '',
        year: '',
        data_uri: null,
    };
  },

    componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/edit_car',
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

        //console.log(data)

        $.ajax({
            type: "POST",
            url: '/edit_car',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            //error: this.handleSubmitFailure,
            dataType: 'json',
            success: this.changepage
		});
    },

    changepage: function (result) {
        //console.log(result);
        //console.log(result.brand);
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

    handleFile: function(e) {
        var self = this;
        var reader = new FileReader();
        var file = e.target.files[0];

        reader.onload = function(upload) {
            self.setState({
                data_uri: upload.target.result,
            });
        }
        reader.readAsDataURL(file);
    },

    handleImages: function (e) {
        e.preventDefault()
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

ReactDOM.render(<AddCar />, editcar);

var Association = React.createClass({
    
    getInitialState: function() {
    return{
        listofdealeships: [],
        selecteddealership: '0',
    };
  },

    componentDidMount: function() {

        $.ajax({
            type: "GET",
            url: '/listdealershipsbydonthavecar',
            data: '',
            //error: this.handleSubmitFailure,
            success: this.changeDealership

		});
  },

    associateDealership: function (e){
        e.preventDefault()
        //console.log('dealership: '+this.state.selecteddealership);

        var data = {
            selecteddealership: this.state.selecteddealership,
        }

        $.ajax({
            type: "POST",
            url: '/associatecaranddealership',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            //error: this.handleSubmitFailure,
            success: this.changeDealership
		});
    },

    changeDealership: function (result) {
        //console.log(result.data);
        this.setState({
            listofdealeships: result.data
        });
        /*console.log(this.state.listofdealeships);*/
    },

    changeSelectedDealership: function (e) {
        this.setState({
            selecteddealership: e.target.value
        });
    },

    createlistdealerships: function (item, id) {
        //console.log(item.id);
        return (<option value={item.id}>{item.name}</option>)
    },

    
    render: function() {
        return (
            <div id="assocation">
            <h3>Associate Car to Dealership</h3>
                <form onSubmit={this.associateDealership}>
                    <select name="play" onChange={this.changeSelectedDealership} value={this.state.selecteddealership}>
                        <option value="50"> </option>
                        {this.state.listofdealeships.map(this.createlistdealerships)}
                    </select>
                    <input type="submit" value="Associate"/>
                </form>
            </div>
      )
    }
});

ReactDOM.render(<Association />, association);

var Desassociation = React.createClass({

    getInitialState: function() {
    return{
        listofdealeships: [],
        selecteddealership: '0',
    };
  },

    componentDidMount: function() {

        $.ajax({
            type: "GET",
            url: '/listdealershipsbyhavingcar',
            data: '',
            //error: this.handleSubmitFailure,
            success: this.changeDealership

		});
  },

    associateDealership: function (e){
        e.preventDefault()
        //console.log('dealership: '+this.state.selecteddealership);


        var data = {
            selecteddealership: this.state.selecteddealership,
        }

        $.ajax({
            type: "POST",
            url: '/dissociatecaranddealership',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            //error: this.handleSubmitFailure,
            success: this.changeDealership
		});
    },

    changeDealership: function (result) {
        //console.log(result.data);
        this.setState({
            listofdealeships: result.data
        });
        /*console.log(this.state.listofdealeships);*/
    },

    changeSelectedDealership: function (e) {
        this.setState({
            selecteddealership: e.target.value
        });
    },

    createlistdealerships: function (item, id) {
        //console.log(item.id);
        return (<option value={item.id}>{item.name}</option>)
    },


    render: function() {
        return (
            <div id="Dissocation">
            <h3>Dissociate Car from Dealership</h3>
                <form onSubmit={this.associateDealership}>
                    <select name="play" onChange={this.changeSelectedDealership} value={this.state.selecteddealership}>
                        <option value="50"> </option>
                        {this.state.listofdealeships.map(this.createlistdealerships)}
                    </select>
                    <input type="submit" value="Dissociate"/>
                </form>
            </div>
      )
    }
});

ReactDOM.render(<Desassociation />, dissociation);