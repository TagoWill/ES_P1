var MyCars = React.createClass({

    getInitialState: function() {
    return{
        listofcars: [],
        listofdealeships: [],
        dl_search: '',
        selectedcar: '1',
        selecteddealership: '1',
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

                /*for (var i = 0; i < resulte.data.length; i++) {
                    var option = resulte.data[i];
                    console.log(option);
                    this.state.listofdealeships.push(
                        <option key={i} value={option.id}>{option.name}</option>
                    );
                }*/

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
      )
    }
});

ReactDOM.render(<MyCars />, list_mycars);