import React from 'react';
import { connect } from 'react-redux';

import RepoAppSettingsTab from '../components/repo_app_settings_tab'

class RepoSettingsApp extends React.Component{
  componentDidMount(){

  }

  render() {
    const { params } = this.props;
    let owner = params.owner;
    let repo = params.repo;

    return (
      <RepoAppSettingsTab owner={owner} repo={repo} />
    );
  }
}

function mapStateToProps(state){
  return {
  }
}

export default connect(mapStateToProps)(RepoSettingsApp)