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
            // eslint-disable-next-line no-unused-vars
            let receivedSpecifications = [];

            await SpecificationApi().getSpecifications()
                .then((fullResponse) =>receivedSpecifications =  mapReceivedSpecs(fullResponse))
                .catch((error) => PubSub.publish("networkError",
                    {title: "Problem while fetching specifications",error}));

            return dispatch({type: AppContextActions.LOAD_SPECIFICATIONS,
                payload:
                    {specifications:
                            {specifications: receivedSpecifications,
                                hasLoaded: true}}});
        },[dispatch]

    );

    function mapReceivedSpecs(fullResponse){
        return fullResponse?.data?.apis?.map((receivedSpec)=>{
           return  { label:receivedSpec?.id, value : receivedSpec?.id, link: receivedSpec?.spec_url};});
    }
    const value = {
        appState,
        setSelectedSpecification,
        loadSpecifications
    };
    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export {AppContext, AppContextProvider, useAppContext};
