import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

function user_reducer(state={
    profile: {
        user_name: null,
        user_description: null
    }
}, action){
    switch(action.type){
        default:
            return state;
    }
}

const userAppReducer = combineReducers({
    user:user_reducer,
    routing
});

export default userAppReducer;