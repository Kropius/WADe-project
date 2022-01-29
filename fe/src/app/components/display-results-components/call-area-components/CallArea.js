import React, {useEffect, useState} from "react";
import {Button} from "@awsui/components-react";


const CallArea = ({selectedApi, path, queryParams, requestBody, verb}) =>{
    // const [isValid, setIsValid] = useState(true);
    const [selecteedApi, setSelecteedApi] = useState(null);

    useEffect(()=>{
        setSelecteedApi(selectedApi);
    },[]);

    useEffect(()=>{
        performRequest();
    });


    function performRequest(){
        const fullPath = selecteedApi?.link + [path,queryParams].filter((pathItem)=> pathItem!=="N/A").join("");
        console.log(fullPath, requestBody, verb);
    }

    return(
        <div>

        <Button variant="primary" iconAlign="right"
                iconName="external">Call with the above parameters to {selecteedApi?.label}</Button>
        </div>
    );
};

export default CallArea;
