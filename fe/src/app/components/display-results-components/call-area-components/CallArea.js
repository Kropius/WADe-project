import React, {useEffect, useState} from "react";
import {Button} from "@awsui/components-react";
import CallAreaConfigurations from "./CallAreaConfigurations";


const CallArea = ({selectedApi, path, queryParams, requestBody, verb}) =>{
    // const [isValid, setIsValid] = useState(true);
    const [selecteedApi, setSelecteedApi] = useState(null);
    useEffect(()=>{
        setSelecteedApi(selectedApi);
    },[]);

    function performRequest(){
        const fullPath = selecteedApi?.url + [path,queryParams].filter((pathItem)=> pathItem!=="N/A").join("");
        if(verb)CallAreaConfigurations.performCall(verb,fullPath, null,  requestBody);
    }

    return(
        <div>

        <Button variant="primary" iconAlign="right"
                iconName="external"
        onClick={performRequest}>
            Call with the above parameters to {selecteedApi?.label}
         </Button>
        </div>
    );
};

export default CallArea;
