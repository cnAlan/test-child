import React from 'react';
import PropTypes from 'prop-types'
import { connect } from 'react-redux';

import {fetchOrgMembers} from '../actions'

import OrgMemberList from '../components/OrgMemberList'

export class OrgPeopleApp extends React.Component{
    componentDidMount(){
        const { dispatch, params } = this.props;
        let owner = params.owner;
        dispatch(fetchOrgMembers(owner))
    }

    render() {
        const { member_list, params } = this.props;
        let owner = params.owner;
        return (
            <div>
                <div className="col-md-12">
                    <h2>人员</h2>
                    <OrgMemberList member_list={member_list} owner={owner} />
                </div>
            </div>
        );
    }
}

OrgPeopleApp.propTypes = {
    member_list: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired
    }).isRequired).isRequired
};

function mapStateToProps(state){
    return {
        member_list: state.orgMembers.members
    }
}

export default connect(mapStateToProps)(OrgPeopleApp)