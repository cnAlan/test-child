import { combineReducers } from 'redux'

// watch

export const POST_DING_TALK_WARNING_WATCHER_USER = 'POST_DING_TALK_WARNING_WATCHER_USER';

export function requestDingTalkWarningWatcherUser(owner, repo, user){
    return {
        type: POST_DING_TALK_WARNING_WATCHER_USER,
        owner,
        repo,
        user
    }
}

export function fetchDingTalkWarningWatcherUser(owner, repo, user) {
    return function (dispatch) {
        dispatch(requestDingTalkWarningWatcherUser(owner, repo, user));
        return fetch('/api/v2/repos/' + owner + '/' + repo + '/warning/dingtalk/watch/watcher/' + user, {
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

export function requestDeleteDingTalkWarningWatcherUser(owner, repo, user){
    return {
        type: DELETE_DING_TALK_WARNING_WATCHER_USER,
        owner,
        repo,
        user
    }
}

export function fetchDeleteDingTalkWarningWatcherUser(owner, repo, user) {
    return function (dispatch) {
        dispatch(requestDeleteDingTalkWarningWatcherUser(owner, repo, user));
        return fetch('/api/v2/repos/' + owner + '/' + repo + '/warning/dingtalk/watch/watcher/' + user, {
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