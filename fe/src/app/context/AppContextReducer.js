import AppContextActions from "./AppContextActions";

function AppContextReducer(state, action){
    const {type, payload} = action;
    switch (type){
        case AppContextActions.SET_SELECTED_SPECIFICATION:{
            console.log("Setting selected specification", state, payload);
            return {...state, ...payload};
        }

        case AppContextActions.LOAD_SPECIFICATIONS:{
            console.log("Setting all specifications", state, payload);
            return {...state, ...payload};
        }

        case AppContextActions.ADD_NEW_RESPONSE:{
            console.log("Adding new response", state, payload);
            state?.receivedNLPResults.append(payload);
            return state;
        }

        default:{
            return {...state, ...payload};
        }}
}

export default AppContextReducer;
