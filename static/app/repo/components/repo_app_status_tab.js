import React from 'react';
import PropTypes from 'prop-types'

export default class RepoAppStatusTab extends React.Component{
  constructor(props) {
    super(props);
  }
  render() {
    let owner = this.props.owner;
    let repo = this.props.repo;
    return (
      <section className="row">
        Status Tab
      </section>
    );
  }
}

RepoAppStatusTab.propTypes = {
  owner: PropTypes.string.isRequired,
  repo: PropTypes.string.isRequired
};
