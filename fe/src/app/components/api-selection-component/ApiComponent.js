import React, {useEffect} from "react";
import { SpaceBetween } from "@awsui/components-react";
import SelectionComponent from "./select-api-component/SelectionComponent";
import SwaggerComponent from "./swagger-component/SwaggerComponent";
import "./swagger-component/SwaggerWidget.module.css";
import {useAppContext} from "../../context/AppContext";

const ApiComponent = () => {
    // const [selectedApi, setSelectedApi] = useState("");
    const {appState, setSelectedSpecification, loadSpecifications} = useAppContext();

    useEffect(()=>{
        if(!appState?.specifications?.hasLoaded){

            loadSpecifications();
        }
    }, []);

    return (
        <SpaceBetween size="l" direction="vertical">
            <SelectionComponent handleApiSelection={setSelectedSpecification}
                                options={appState?.specifications?.specifications}/>
            <SwaggerComponent apiLink={appState?.selectedSpecification?.link}
                              title={appState?.selectedSpecification?.label ?? "No specification selected"} />
        </SpaceBetween>
    );
};
export default ApiComponent;
