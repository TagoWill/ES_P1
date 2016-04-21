var DealershipDetails = React.createClass({
    getInitialState: function() {
        return{
            listofcars: [],
            info: [],
            selectedcar: '1'
        };
    },

    componentDidMount: function() {
        $.ajax({
            type: "GET",
            url: '/listmydealershipdetails',
            data: '',
            //error: this.handleSubmitFailure,
            success: this.changepage
        });

        $.ajax({
            type: "GET",
            url: '/listmydealershipdetails2',
            data2: '',
            //error: this.handleSubmitFailure,
            success: this.changepage2
        });
    },

    changepage: function (result) {
        this.setState({
            listofcars: result.data
        });
    },

    changepage2: function (result2) {
        this.setState({
            info: result2.data2
        });
    },

    createinfo: function (item) {
        var infotext = [
            <h2>Name: {item.name}</h2>,
            <h3>Location: {item.district}</h3>];
        return (<div><br>{infotext}</br></div>)
    },

    createlistcars: function (item) {
        var linha = [
            <td><img src={"/static/image/"+item.id + ".jpg"} alt="pic1" height="100" width="120"/></td>,
            <td>{item.brand}</td>,
            <td>{item.model}</td>,
            <td>{item.fuel}</td>,
            <td>{item.price}€</td>,
            <td>{item.kms}</td>,
            <td>{item.year}</td>]
        return (<tr>{linha}</tr>)
    },

    render: function() {
        return (
            <div>
                {this.state.info.map(this.createinfo)}
                <table>
                    <thead>
                        <tr>
                            <td>Image</td>
                            <td>Brand</td>
                            <td>Model</td>
                            <td>Fuel</td>
                            <td>Price</td>
                            <td>Kilometers</td>
                            <td>Year</td>
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

ReactDOM.render(<DealershipDetails/>, dealershipdetails);

