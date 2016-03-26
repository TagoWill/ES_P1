/**
 * Created by dbast on 07/03/2016.
 */

var Home = React.createClass({
    render: function() {
        return <div>Hello {this.props.name}</div>;
    }
});

ReactDOM.render(<Home name="Daniel" />, content);