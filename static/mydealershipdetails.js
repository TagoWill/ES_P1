var MyDealershipDetails = React.createClass({
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
            <h2>{item.name} Details</h2>,
            <h3>Location: {item.district}</h3>];
        return (<div>{infotext}</div>)
    },

    createlistcars: function (item) {
        var linha = [
            <td><img src={"/static/image/"+item.id + ".jpg"} alt="pic1" height="100" width="120"/></td>,
            <td>
                <a href={'detailcar?id='+item.id}>{item.brand}</a></td>,
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
            {this.state.info.map(this.createinfo)}
            <table>
                <thead>
                <tr>
                    <th>Image</th>
                    <th>Brand</th>
                    <th>Model</th>
                    <th>Fuel</th>
                    <th>Price</th>
                    <th>Kilometers</th>
                    <th>Year</th>
                    <th>Edit</th>
                    <th>Delete</th>
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

ReactDOM.render(<MyDealershipDetails/>, mydealershipdetails);

