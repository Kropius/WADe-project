import React, {useCallback} from "react";
import {createContext, useContext, useReducer} from "react";
import AppContextReducer from "./AppContextReducer";
import AppContextInitData from "./AppContextInitData";
import AppContextActions from "./AppContextActions";
import SpecificationApi from "../api/SpecificationApi";
import PubSub from "pubsub-js";

const useAppContext = () => useContext(AppContext);

const AppContext = createContext();

function AppContextProvider({children}){
    const [appState, dispatch] = useReducer(AppContextReducer, AppContextInitData);

    const setSelectedSpecification = (selectedSpecification) =>{
        return dispatch({
            type: AppContextActions.SET_SELECTED_SPECIFICATION,
            payload:{
                selectedSpecification
            }
        });
    };

    const loadSpecifications = useCallback(
        async() => {
            console.log("executing load specifications");
            // eslint-disable-next-line no-unused-vars
            let receivedSpecifications = [];
            const mockedOptions = [{
                "label": "Petstore",
                "value": "1",
                "link": "https://petstore.swagger.io/v2/swagger.json"
            }, {
                "label": "WadeProject",
                "value": "2",
                "link": "https://raw.githubusercontent.com/Kropius/WADe-project/main/documentation/OpenApi/openapi.json"
            }, {
                "label": "School API",
                "value": "3",
                "link": "https://petstore.swagger.io/v2/swagger.json"
            }];
            await SpecificationApi().getSpecifications()
                .then((fullResponse) =>receivedSpecifications = fullResponse?.data?.data)
                .catch((error) => PubSub.publish("networkError",
                    {title: "Problem while fetching specifications",error }));

            console.log(receivedSpecifications);
            return dispatch({type: AppContextActions.LOAD_SPECIFICATIONS,
                payload:
                    {specifications:
                            {specifications: mockedOptions,
                                hasLoaded: true}}});
        },[dispatch]

    );


    const value = {
        appState,
        setSelectedSpecification,
        loadSpecifications
    };
    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export {AppContext, AppContextProvider, useAppContext};
