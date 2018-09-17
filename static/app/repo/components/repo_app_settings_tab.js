import React from 'react';
import PropTypes from 'prop-types'

export default class RepoAppSettingsTab extends React.Component{
  constructor(props) {
    super(props);
  }
  render() {
    let owner = this.props.owner;
    let repo = this.props.repo;
    return (
      <section className="row">
        Settings Tab
      </section>
    );
  }
}

RepoAppSettingsTab.propTypes = {
  owner: PropTypes.string.isRequired,
  repo: PropTypes.string.isRequired
};
