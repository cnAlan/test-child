import React from 'react';
import PropTypes from 'prop-types'

export default class WarnPolicyPanel extends React.Component{
  constructor(props) {
    super(props);
  }

  render() {
    const { id, owner, repo} = this.props;
    return (
      <div>
        <h4 id={id}>报警策略设置</h4>
        <p>有新的任务出错就会发送报警信息</p>
      </div>
    );
  }
}

WarnPolicyPanel.propTypes = {
  id: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  owner: PropTypes.string.isRequired,
  repo: PropTypes.string.isRequired
};