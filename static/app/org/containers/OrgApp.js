import React from 'react';
import { connect } from 'react-redux';

import PageHeader from '../../base/components/page_header'
import OrgAppTitle from '../components/OrgAppTitle'
import OrgAppNaviBar from '../components/OrgAppNaviBar'

class OrgApp extends React.Component{
    componentDidMount(){

    }

    render() {
        const { params } = this.props;
        let owner = params.owner;

        let url = {
            index_page: '/'
        };

        return (
            <div>
                <PageHeader url={ url }/>

                <OrgAppTitle owner={owner} />

                <OrgAppNaviBar owner={owner} />

                {this.props.children}

            </div>
        );
    }
}


function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(OrgApp)