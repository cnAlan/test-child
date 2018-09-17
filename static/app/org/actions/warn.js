import { combineReducers } from 'redux'

export const REQUEST_DING_TALK_WARNING_WATCH_USERS = 'REQUEST_DING_TALK_WARNING_WATCH_USERS';

export function requestDingTalkWarningWatchUsers(owner){
    return {
        type: REQUEST_DING_TALK_WARNING_WATCH_USERS,
        owner
    }
}

export function fetchDingTalkWarningWatchUsers(owner) {
    return function (dispatch) {
        dispatch(requestDingTalkWarningWatchUsers(owner));
        return fetch('/api/v2/orgs/' + owner + '/warning/dingtalk/watch/watchers')
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

export function requestDingTalkWarningSuggestedUsers(owner){
    return {
        type: REQUEST_DING_TALK_WARNING_SUGGESTED_USERS,
        owner
    }
}

export function fetchDingTalkWarningSuggestedUsers(owner) {
    return function (dispatch) {
        dispatch(requestDingTalkWarningSuggestedUsers(owner));
        return fetch('/api/v2/orgs/' + owner + '/warning/dingtalk/watch/watchers/suggested')
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




// watch

export const POST_DING_TALK_WARNING_WATCHER_USER = 'POST_DING_TALK_WARNING_WATCHER_USER';

export function requestDingTalkWarningWatcherUser(owner, user){
    return {
        type: POST_DING_TALK_WARNING_WATCHER_USER,
        owner,
        user
    }
}

export function fetchDingTalkWarningWatcherUser(owner, user) {
    return function (dispatch) {
        dispatch(requestDingTalkWarningWatcherUser(owner, user));
        return fetch('/api/v2/orgs/' + owner + '/warning/dingtalk/watch/watcher/' + user, {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => dispatch(receiveDingTalkWarningWatcherUserSuccess({
                    data: data
            })))
    };
}


export const RECEIVE_DING_TALK_WARNING_WATCHER_USER_FAILURE = 'RECEIVE_DING_TALK_WARNING_WATCHER_USER_FAILURE';
export function receiveDingTalkWarningWatcherUserFailure(error){
    return {
        type: RECEIVE_DING_TALK_WARNING_WATCHER_USER_FAILURE,
        error
    }
}


export const RECEIVE_DING_TALK_WARNING_WATCHER_USER_SUCCESS = 'RECEIVE_DING_TALK_WARNING_WATCHER_USER_SUCCESS';
/**
 *
 * @param response
 *      {
 *          data:[]
 *      }
 * @returns {{type: string, response: *, receive_time: number}}
 */
export function receiveDingTalkWarningWatcherUserSuccess(response) {
    return {
        type: RECEIVE_DING_TALK_WARNING_WATCHER_USER_SUCCESS,
        response,
        receive_time: Date.now()
    }
}


// unwatch

export const DELETE_DING_TALK_WARNING_WATCHER_USER = 'DELETE_DING_TALK_WARNING_WATCHER_USER';

export function requestDeleteDingTalkWarningWatcherUser(owner, user){
    return {
        type: DELETE_DING_TALK_WARNING_WATCHER_USER,
        owner,
        user
    }
}

export function fetchDeleteDingTalkWarningWatcherUser(owner, user) {
    return function (dispatch) {
        dispatch(requestDeleteDingTalkWarningWatcherUser(owner, user));
        return fetch('/api/v2/orgs/' + owner + '/warning/dingtalk/watch/watcher/' + user, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => dispatch(receiveDeleteDingTalkWarningWatcherUserSuccess({
                    data: data
            })))
    };
}


export const RECEIVE_DELETE_DING_TALK_WARNING_WATCHER_USER_FAILURE = 'RECEIVE_DELETE_DING_TALK_WARNING_WATCHER_USER_FAILURE';
export function receiveDeleteDingTalkWarningWatcherUserFailure(error){
    return {
        type: RECEIVE_DELETE_DING_TALK_WARNING_WATCHER_USER_FAILURE,
        error
    }
}


export const RECEIVE_DELETE_DING_TALK_WARNING_WATCHER_USER_SUCCESS = 'RECEIVE_DELETE_DING_TALK_WARNING_WATCHER_USER_SUCCESS';
/**
 *
 * @param response
 *      {
 *          data:[]
 *      }
 * @returns {{type: string, response: *, receive_time: number}}
 */
export function receiveDeleteDingTalkWarningWatcherUserSuccess(response) {
    return {
        type: RECEIVE_DELETE_DING_TALK_WARNING_WATCHER_USER_SUCCESS,
        response,
        receive_time: Date.now()
    }
}