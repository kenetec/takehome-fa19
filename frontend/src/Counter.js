import React, { Component } from 'react'

class Counter extends Component {
  // YOUR CODE GOES BELOW
  constructor(props) {
    super(props);

    this.state = {count: props.count};
  }

  // componentWillReceiveProps() found from https://stackoverflow.com/questions/32414308/updating-state-on-props-change-in-react-form
  componentWillReceiveProps(props) {
    if (this.state.count != props.count) {
      this.setState({
        count: props.count
      });
    }
  }

  incrementCount = (e) => {
    e.preventDefault();

    this.setState({count: ++this.state.count});
  }

  decrementCount = (e) => {
    e.preventDefault();

    this.setState({count: --this.state.count});
  }
  
  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button name="incrementCount" onClick={this.incrementCount}>Increment</button><br/>
        <button name="decrementCount" onClick={this.decrementCount}>Decrement</button>
      </div>
    )
  }
}

export default Counter
