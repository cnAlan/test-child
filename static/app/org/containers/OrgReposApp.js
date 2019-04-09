import React from 'react';
import PropTypes from 'prop-types'
import { connect } from 'react-redux';

import {fetchOrgRepos, fetchOrgMembers} from '../actions'

import OrgRepoList from '../components/OrgRepoList'
import OrgMemberList from '../components/OrgMemberList'

export class OrgReposApp extends React.Component{
  componentDidMount(){
    const { dispatch, params } = this.props;
    let owner = params.owner;
    console.log('OrgReposApp:', owner);
    dispatch(fetchOrgRepos(owner));
    dispatch(fetchOrgMembers(owner))
  }

  render() {
    const { repo_list, member_list, params } = this.props;
    let owner = params.owner;
    return (
      <div className="row">
        <div className="col-md-8">
          <h2>项目</h2>
          <OrgRepoList repo_list={repo_list} owner={owner} />
        </div>
        <div className="col-md-4">
          <h2>人员</h2>
          <OrgMemberList member_list={member_list} owner={owner} />
        </div>
      </div>
    );
  }
}

OrgReposApp.propTypes = {
  repo_list: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired
  }).isRequired).isRequired,
  member_list: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired
  }).isRequired).isRequired
};

function mapStateToProps(state){
  return {
    repo_list: state.orgRepos.repos,
    member_list: state.orgMembers.members
  }
}

export default connect(mapStateToProps)(OrgReposApp)