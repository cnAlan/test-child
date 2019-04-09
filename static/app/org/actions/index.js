import { combineReducers } from 'redux'
import fetch from 'isomorphic-fetch'

export const REQUEST_ORG_REPOS = 'REQUEST_ORG_REPOS';
export function requestOrgRepos(owner){
    return {
        type: REQUEST_ORG_REPOS,
        owner
    }
}

export function fetchOrgRepos(owner) {
    return function (dispatch) {
        dispatch(requestOrgRepos(owner));
        return fetch('/api/v2/orgs/' + owner + '/repos')
            .then(response => response.json())
            .then(data => dispatch(receiveOrgReposSuccess({
                    data: data
            })))
    };
}


export const RECEIVE_ORG_REPOS_FAILURE = 'RECEIVE_ORG_REPOS_FAILURE';
export function receiveOrgReposFailure(error){
    return {
        type: RECEIVE_ORG_REPOS_FAILURE,
        error
    }
}


export const RECEIVE_ORG_REPOS_SUCCESS = 'RECEIVE_ORG_REPOS_SUCCESS';
/**
 *
 * @param response
 *      {
 *          data:[]
 *      }
 * @returns {{type: string, response: *, receive_time: number}}
 */
export function receiveOrgReposSuccess(response) {
    return {
        type: RECEIVE_ORG_REPOS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}



export const REQUEST_ORG_MEMBERS = 'REQUEST_ORG_MEMBERS';

export function requestOrgMembers(owner){
    return {
        type: REQUEST_ORG_MEMBERS,
        owner
    }
}

export function fetchOrgMembers(owner) {
    return function (dispatch) {
        dispatch(requestOrgMembers(owner));
        return fetch('/api/v2/orgs/' + owner + '/members')
            .then(response => response.json())
            .then(data => dispatch(receiveOrgMembersSuccess({
                    data: data
            })))
    };
}

export const RECEIVE_ORG_MEMBERS_SUCCESS = 'RECEIVE_ORG_MEMBERS_SUCCESS';
/**
 *
 * @param response
 *      {
 *          data:[]
 *      }
 * @returns {{type: string, response: *, receive_time: number}}
 */
export function receiveOrgMembersSuccess(response) {
    return {
        type: RECEIVE_ORG_MEMBERS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}