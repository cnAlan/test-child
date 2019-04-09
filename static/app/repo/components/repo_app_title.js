import React from 'react';
import PropTypes from 'prop-types'

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import {faBook} from '@fortawesome/fontawesome-free-solid'

export default class RepoAppTitle extends React.Component{
  constructor(props) {
    super(props);
  }
  render() {
    let owner = this.props.owner;
    let repo = this.props.repo;
    return (
      <section className="row">
        <h1>
          <FontAwesomeIcon icon={faBook} />
          <a href={ '/' + owner }>{ owner }</a>/<a href={ '/' + owner + '/' + repo }>{ repo }</a>
        </h1>
      </section>
    );
  }
}

RepoAppTitle.propTypes = {
  owner: PropTypes.string.isRequired,
  repo: PropTypes.string.isRequired
};
