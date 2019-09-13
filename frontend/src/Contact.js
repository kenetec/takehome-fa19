import React, { Component } from 'react'

class App extends Component {
  // YOUR CODE GOES BELOW
  constructor(props) {
    super(props);

    this.state = {
      id: props.id,
      name: props.name,
      nickname: props.nickname,
      hobby: props.hobby,
    };
  }
  
  render() {
    return (
      <div>
        <p>{this.state.name}</p>
      </div>
    )
  }
}

export default App
