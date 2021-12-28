import React, {useState} from "react";
import {SpaceBetween} from "@awsui/components-react";
import SelectionComponent from "./select-api-component/SelectionComponent";
import SwaggerComponent from "./swagger-component/SwaggerComponent";
import "./swagger-component/SwaggerWidget.module.css";
const ApiComponent = () =>{
    const [selectedApi, setSelectedApi] = useState("")
    return (
        <SpaceBetween size="l" direction="vertical">
            <SelectionComponent handleApiSelection = {setSelectedApi}/>
            <SwaggerComponent apiLink={selectedApi.link} title={selectedApi.label}/>
        </SpaceBetween>
    )
}
export default ApiComponent;
