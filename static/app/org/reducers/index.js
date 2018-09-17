import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

import { REQUEST_ORG_REPOS, RECEIVE_ORG_REPOS_SUCCESS,
    REQUEST_ORG_MEMBERS, RECEIVE_ORG_MEMBERS_SUCCESS
} from '../actions'



/* reducer */

//const initialState = {
//    org_repo_list: []
//};

/**
 *
 * @param state
 *      state of orgRepos:
 *      {
 *          status: {
 *              is_fetching: boolean,
 *              last_updated: number // Date()
 *          }
 *          owner: string
 *          repos: array of repo object
 *              [
 *                  { id: number, name: string },
 *                  ...
 *              ]
 *
 *      }
 * @param action
 * @returns {*}
 */

function orgRepos(state = {
    status:{
        is_fetching: false,
        last_updated: null
    },
    owner: 'nwp_xp',
    repos: []
}, action){
    switch(action.type){
        case REQUEST_ORG_REPOS:
            console.log(action.owner);
            return Object.assign({}, state, {
                status: {
                    is_fetching: true,
                    last_updated: state.status.last_updated
                }
            });
        case RECEIVE_ORG_REPOS_SUCCESS:
            return Object.assign({}, state, {
                repos: action.response.data.data.repos,
                status: {
                    is_fetching: false,
                    last_updated: action.receive_time
                }
            });
        default:
            return state;
    }
}


/**
 *
 * @param state
 *      state of orgRepos:
 *      {
 *          status: {
 *              is_fetching: boolean,
 *              last_updated: number // Date()
 *          }
 *          owner: string
 *          members: array of member object
 *              [
 *                  { id: number, name: string },
 *                  ...
 *              ]
 *
 *      }
 * @param action
 * @returns {*}
 */
function orgMembers(state = {
    status:{
        is_fetching: false,
        last_updated: null
    },
    owner: 'nwp_xp',
    members: []
}, action){
    switch(action.type){
        case REQUEST_ORG_MEMBERS:
            console.log(action.owner);
            return Object.assign({}, state, {
                status: {
                    is_fetching: true,
                    last_updated: state.status.last_updated
                }
            });
        case RECEIVE_ORG_MEMBERS_SUCCESS:
            return Object.assign({}, state, {
                members: action.response.data.data.members,
                status: {
                    is_fetching: false,
                    last_updated: action.receive_time
                }
            });
        default:
            return state;
    }
}

// warning reducer
import {
    REQUEST_DING_TALK_WARNING_WATCH_USERS,
    RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS,
    RECEIVE_DING_TALK_WARNING_WATCH_USERS_FAILURE,
    REQUEST_DING_TALK_WARNING_SUGGESTED_USERS,
    RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS,
    RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_FAILURE,
} from '../actions/warn'

function ding_talk_watching_user_reducer(state={
    owner: null,
    repo_count: 0,
    watching_user_list: []
}, action){
    switch (action.type) {
        case RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS:
            return Object.assign({}, state, {
                owner: action.response.data.data.owner,
                repo_count: action.response.data.data.repo_count,
                watching_user_list: action.response.data.data.warning.watching_user_list
            });
        default:
            return state;
    }
}

function ding_talk_suggested_user_reducer(state={
    owner: null,
    suggested_user_list: []
}, action){
    switch (action.type) {
        case RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS:
            return Object.assign({}, state, {
                owner: action.response.data.data.owner,
                repo_count: action.response.data.data.repo_count,
                suggested_user_list: action.response.data.data.warning.suggested_user_list
            });
        default:
            return state;
    }
}

function ding_talk_reducer(state = {
    watching_user: {
        owner: null,
        repo_count: 0,
        watching_user_list: []
    },
    suggested_user: {
        owner: null,
        suggested_user_list: []
    }
}, action) {
    switch (action.type) {
        case RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS:
            return Object.assign({}, state, {
                watching_user: ding_talk_watching_user_reducer(state.watching_user, action)
            });
        case RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS:
            return Object.assign({}, state, {
                suggested_user: ding_talk_suggested_user_reducer(state.suggested_user, action)
            });
        default:
            return state;
    }
}


function warning_reducer(state={
    ding_talk:{
        watching_user: {
            owner: null,
            repo_count: 0,
            watching_user_list: []
        },
        suggested_user: {
            owner: null,
            suggested_user_list: []
        }
    }
}, action){
    switch(action.type){
        case RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS:
        case RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS:
            return Object.assign({}, state, {
                ding_talk: ding_talk_reducer(state.ding_talk, action)
            });
        default:
            return state;
    }
}

const orgAppReducer = combineReducers({
    orgRepos,
    orgMembers,
    warning: warning_reducer,
    routing
});

export default orgAppReducer;