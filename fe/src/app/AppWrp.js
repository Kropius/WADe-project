import React from "react";
import {AppContextProvider} from "./context/AppContext";
import App from "./App";
import AlertService from "./alerts/AlertService";


const AppWrp = () => {
    return (
        <React.StrictMode>
            <AppContextProvider>
                <AlertService/>
                <App key={"App"}/>
            </AppContextProvider>
        </React.StrictMode>
    );
};

export default  AppWrp;
