import { combineReducers } from 'redux'

export const REQUEST_DING_TALK_WARNING_WATCH_USERS = 'REQUEST_DING_TALK_WARNING_WATCH_USERS';

export function requestDingTalkWarningWatchUsers(owner, repo){
    return {
        type: REQUEST_DING_TALK_WARNING_WATCH_USERS,
        owner,
        repo
    }
}

export function fetchDingTalkWarningWatchUsers(owner, repo) {
    return function (dispatch) {
        dispatch(requestDingTalkWarningWatchUsers(owner, repo));
        return fetch('/api/v2/repos/' + owner + '/' + repo + '/warning/dingtalk/watch/watchers')
            .then(response => response.json())
            .then(data => dispatch(receiveDingTalkWarningWatchUsersSuccess({
                    data: data
            })))
    };
}


export const RECEIVE_DING_TALK_WARNING_WATCH_USERS_FAILURE = 'RECEIVE_DING_TALK_WARNING_WATCH_USERS_FAILURE';
export function receiveDingTalkWarningWatchUsersFailure(error){
    return {
        type: RECEIVE_DING_TALK_WARNING_WATCH_USERS_FAILURE,
        error
    }
}


export const RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS = 'RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS';
/**
 *
 * @param response
 *      {
 *          data:[]
 *      }
 * @returns {{type: string, response: *, receive_time: number}}
 */
export function receiveDingTalkWarningWatchUsersSuccess(response) {
    return {
        type: RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}


// suggested user

export const REQUEST_DING_TALK_WARNING_SUGGESTED_USERS = 'REQUEST_DING_TALK_WARNING_SUGGESTED_USERS';

export function requestDingTalkWarningSuggestedUsers(owner, repo){
    return {
        type: REQUEST_DING_TALK_WARNING_SUGGESTED_USERS,
        owner,
        repo
    }
}

export function fetchDingTalkWarningSuggestedUsers(owner, repo) {
    return function (dispatch) {
        dispatch(requestDingTalkWarningSuggestedUsers(owner, repo));
        return fetch('/api/v2/repos/' + owner + '/' + repo + '/warning/dingtalk/watch/watchers/suggested')
            .then(response => response.json())
            .then(data => dispatch(receiveDingTalkWarningSuggestedUsersSuccess({
                    data: data
            })))
    };
}


export const RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_FAILURE = 'RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_FAILURE';
export function receiveDingTalkWarningSuggestedUsersFailure(error){
    return {
        type: RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_FAILURE,
        error
    }
}


export const RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS = 'RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS';
/**
 *
 * @param response
 *      {
 *          data:[]
 *      }
 * @returns {{type: string, response: *, receive_time: number}}
 */
export function receiveDingTalkWarningSuggestedUsersSuccess(response) {
    return {
        type: RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}