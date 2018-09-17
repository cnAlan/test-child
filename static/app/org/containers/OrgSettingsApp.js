import React from 'react';
import { connect } from 'react-redux';

export class OrgSettingsApp extends React.Component{
    componentDidMount(){
    }

    render() {
        const { params } = this.props;
        let owner = params.owner;
        return (
            <div>
                <div className="col-md-12">
                    <h2>设置</h2>
                </div>
            </div>
        );
    }
}

function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(OrgSettingsApp)