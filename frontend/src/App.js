import React, { Component } from 'react'
import Instructions from './Instructions'
import Contact from './Contact'
import Counter from './Counter'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      contacts: [
        {id: 1, name: "Angad", nickname: "greg", hobby: "dirty-ing"},
        {id: 2, name: "Roy", nickname: "uwu", hobby: "weeb"},
        {id: 3, name: "Daniel", nickname: "oppa", hobby: "losing money with options trading"},
      ],

      contactsCount: 0
    }
  }

  createNewContact = (e) => {
    e.preventDefault();

    let form = e.target;
    let newContacts = this.state.contacts.slice();
    let contactName = e.target.name.value;
    let contactHobby = e.target.hobby.value;

    newContacts.push({
      id: newContacts.length + 1,
      name: contactName,
      nickname: contactName.slice(0, 3),
      hobby: contactHobby
    });

    this.setState({
      contacts: newContacts,
      contactsCount: ++this.state.contactsCount,
    });
  }

  render() {
    return (
      <div className="App">
        <Instructions complete={true}/>

        <Counter count={this.state.contactsCount}/>

        {this.state.contacts.map(x => (
          <Contact id={x.id} name={x.name} nickname={x.nickname} hobby={x.hobby} />
        ))}

        <form name="createContactForm" onSubmit={this.createNewContact}>
          <input name="name" type="text" placeholder="Enter name..."/><br/>
          <input name="hobby" type="text" placeholder="Enter hobby..."/><br/>

          <input type="submit" value="Create Contact"/>
        </form>
      </div>
    )
  }
}

export default App
