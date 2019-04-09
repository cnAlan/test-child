import React from 'react';
import PropTypes from 'prop-types'
import { connect } from 'react-redux';

import WatchingPanel from '../../components/warning/WatchingPanel'
import WatcherSettingPanel from '../../components/warning/WatcherSettingPanel'
import WarnPolicyPanel from '../../components/warning/WarnPolicyPanel'

import {
  fetchDingTalkWarningWatchUsers,
  fetchDingTalkWarningSuggestedUsers
} from '../../actions'

import {
  fetchDingTalkWarningWatcherUser,
  fetchDeleteDingTalkWarningWatcherUser
} from '../../actions/watcher'

export class DingTalkWarningApp extends React.Component{
  constructor(props) {
    super(props);
    this.handleWatchClick = this.handleWatchClick.bind(this);
    this.handleUnWatchClick = this.handleUnWatchClick.bind(this);
    this.updateWatcher = this.updateWatcher.bind(this)
  }

  componentDidMount(){
    const { params } = this.props;
    let owner = params.owner;
    let repo = params.repo;
    this.updateWatcher(owner, repo)
  }

  updateWatcher(owner, repo){
    const { dispatch, params } = this.props;
    dispatch(fetchDingTalkWarningWatchUsers(owner,repo));
    dispatch(fetchDingTalkWarningSuggestedUsers(owner, repo));
  }

  handleWatchClick(owner, repo, users) {
    const { dispatch } = this.props;
    users.forEach(function(item, index, array){
      let user = item;
      dispatch(fetchDingTalkWarningWatcherUser(owner, repo, user));
      console.log('handleWatchClick', owner, repo, user);
    });

    this.updateWatcher(owner, repo);
  }

  handleUnWatchClick(owner, repo, users) {
    const { dispatch } = this.props;
    users.forEach(function(item, index, array){
      let user = item;
      dispatch(fetchDeleteDingTalkWarningWatcherUser(owner, repo, user));
      console.log('handleUnWatchClick', owner, repo, user);
    });

    this.updateWatcher(owner, repo);
  }

  render() {
    let owner = this.props.params.owner;
    let repo = this.props.params.repo;
    const { watching_user_list, suggested_user_list } = this.props;
    return (
      <div>
        <h3>钉钉</h3>
        <div>
          <h4 id="warn_ding_talk_overview">概览</h4>
          <div className="row">
            <div className="col-md-6">
              <p>欢迎扫码加入我们的钉钉团队</p>
              <img src="/static/image/ding_talk_invite.png" />
            </div>
            <div className="col-md-6">
              <p>或者通过点击下面的链接加入团队</p>
              <a href="https://t.dingtalk.com/invite/index?code=76b2940f32">
                https://t.dingtalk.com/invite/index?code=76b2940f32
              </a>
            </div>
          </div>
        </div>
        <WatchingPanel
          id="warn_ding_talk_warn_watching_panel"
          owner={ owner }
          repo={ repo }
          type="dingtalk"
          watching_user_list={ watching_user_list }
          watch_click_handler={ this.handleWatchClick }
          unwatch_click_handler={ this.handleUnWatchClick }
        />
        <WatcherSettingPanel
          id="warn_ding_talk_warn_setting_panel"
          owner={ owner }
          repo={ repo }
          type="dingtalk"
          suggested_user_list={ suggested_user_list }
          watch_click_handler={ this.handleWatchClick }
          unwatch_click_handler={ this.handleUnWatchClick }
        />
        <WarnPolicyPanel
          id="warn_ding_talk_warn_policy_panel"
          owner={owner}
          repo={repo}
          type="dingtalk"
        />
      </div>
    );
  }
}

DingTalkWarningApp.propTypes = {
  dispatch: PropTypes.func.isRequired
};

function mapStateToProps(state){
  return {
    type: 'dingtalk',
    watching_user_list: state.repo.warning.ding_talk.watching_user.watching_user_list,
    suggested_user_list: state.repo.warning.ding_talk.suggested_user.suggested_user_list
  }
}

export default connect(mapStateToProps)(DingTalkWarningApp)