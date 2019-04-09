import React from 'react';
import ReactDom, {render} from 'react-dom';

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import '../css/index.css'

class ExploreOwnerApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {owner: ''};
  }

  onChange(e) {
    this.setState({owner: e.target.value});
  }

  handleSubmit(e) {
    e.preventDefault();
    console.log(this.state.owner);
    window.location.href='/'+this.state.owner;
  }

  render() {
    return (
      <div>
        <form className="form-inline" onSubmit={this.handleSubmit.bind(this)}>
          <div className="form-group">
            <input type="text" className="form-control" placeholder="用户名"
                   onChange={this.onChange.bind(this)} value={this.state.owner} />
            <button type="submit" className="btn btn-light">确定</button>
          </div>
        </form>
      </div>
    );
  }
}

render(<ExploreOwnerApp />, document.getElementById('explore-owner-section'));