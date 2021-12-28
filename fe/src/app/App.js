import React, {useState} from "react";
import InputComponent from "./components/input-components/InputComponent";
import {Grid, SpaceBetween} from "@awsui/components-react";
import "swagger-ui-react/swagger-ui.css"
import AppCss from "./App.module.css";
import ApiComponent from "./components/api-selection-component/ApiComponent";
import ResultsContainer from "./components/display-results-components/ResultsContainer";

const App = () => {
    const [newRequest, setNewRequest] = useState({message: "", isRequest: true});
    console.log(newRequest);
    return (
        <div className={AppCss.app}>
            <Grid gridDefinition={[{colspan: 4}, {colspan: 8}]}>
                <SpaceBetween size={"m"}>
                    <InputComponent setNewRequest={setNewRequest}/>
                    <ResultsContainer newRequest = {newRequest}/>
                </SpaceBetween>

                <ApiComponent/>
            </Grid>

        </div>


    )
}
export default App;
