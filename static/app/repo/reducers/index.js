import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

import {
    REQUEST_DING_TALK_WARNING_WATCH_USERS,
    RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS,
    RECEIVE_DING_TALK_WARNING_WATCH_USERS_FAILURE,
    REQUEST_DING_TALK_WARNING_SUGGESTED_USERS,
    RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS,
    RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_FAILURE,
} from '../actions'


function ding_talk_watching_user_reducer(state={
    owner: null,
    repo: null,
    watching_user_list: []
}, action){
    switch (action.type) {
        case RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS:
            return Object.assign({}, state, {
                owner: action.response.data.data.owner,
                repo: action.response.data.data.repo,
                watching_user_list: action.response.data.data.warning.watching_user_list
            });
        default:
            return state;
    }
}

function ding_talk_suggested_user_reducer(state={
    owner: null,
    repo: null,
    suggested_user_list: []
}, action){
    switch (action.type) {
        case RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS:
            return Object.assign({}, state, {
                owner: action.response.data.data.owner,
                repo: action.response.data.data.repo,
                suggested_user_list: action.response.data.data.warning.suggested_user_list
            });
        default:
            return state;
    }
}


function ding_talk_reducer(state = {
    watching_user: {
        owner: null,
        repo: null,
        watching_user_list: []
    },
    suggested_user: {
        owner: null,
        repo: null,
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
            repo: null,
            watching_user_list: []
        },
        suggested_user: {
            owner: null,
            repo: null,
            suggested_user_list: []
        }
    }
}, action) {
    switch (action.type) {
        case RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS:
        case RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS:
            return Object.assign({}, state, {
                ding_talk: ding_talk_reducer(state.ding_talk, action)
            });
        default:
            return state;
    }
}

function repo_reducer(state={
    warning: {
        ding_talk:{
            watching_user: {
                owner: null,
                repo: null,
                watching_user_list: []
            },
            suggested_user: {
                owner: null,
                repo: null,
                suggested_user_list: []
            }
        }
    }
}, action){
    switch(action.type){
        case RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS:
        case RECEIVE_DING_TALK_WARNING_SUGGESTED_USERS_SUCCESS:
            return Object.assign({}, state, {
                warning: warning_reducer(state.warning, action)
            });
        default:
            return state;
    }
}

const repoAppReducer = combineReducers({
    repo:repo_reducer,
    routing
});

export default repoAppReducer;