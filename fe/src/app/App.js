import React, { useState} from "react";
import InputComponent from "./components/input-components/InputComponent";
import { Grid, SpaceBetween } from "@awsui/components-react";
import "swagger-ui-react/swagger-ui.css";
import AppCss from "./App.module.css";
import ApiComponent from "./components/api-selection-component/ApiComponent";
import ResultsContainer from "./components/display-results-components/ResultsContainer";
import {useAppContext} from "./context/AppContext";


const App = () => {
    const [newRequest, setNewRequest] = useState({ message: "", isRequest: true });
    const [isLoading, setIsLoading] = useState(false);

    const {appState} = useAppContext();
    return (
        <div className={AppCss.app}>
            <Grid gridDefinition={[{ colspan: 4 }, { colspan: 8 }]}>
                <SpaceBetween size={"m"}>
                    <InputComponent setNewRequest={setNewRequest} isLoading={isLoading}
                                    selectedApi={appState?.selectedSpecification}/>
                    <ResultsContainer newRequest={newRequest} setIsLoading={setIsLoading}/>
                </SpaceBetween>

                <ApiComponent />
            </Grid>
        </div>
    );
};

export default App;
