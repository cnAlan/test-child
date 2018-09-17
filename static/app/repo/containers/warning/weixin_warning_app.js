import React from 'react';
import { connect } from 'react-redux';

export class WeixinWarningApp extends React.Component{
  constructor(props) {
    super(props);
  }
  render() {
    let owner = this.props.params.owner;
    let repo = this.props.params.repo;
    return (
      <div>
        <h3>微信</h3>
        <div>
          <h4>概览</h4>
        </div>
        <div>
          <h4>人员列表</h4>
        </div>
        <div>
          <h4>推送设置</h4>
        </div>
        <div>
          <h4>报警策略设置</h4>
        </div>
      </div>
    );
  }
}

function mapStateToProps(state){
  return {
  }
}

export default connect(mapStateToProps)(WeixinWarningApp)