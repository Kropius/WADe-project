import React, {useState} from "react";
import {Select} from "@awsui/components-react";

const SelectApi = ({options, selectionHandler}) => {
    const mockedOptions = [{
        "label": "Petstore",
        "value": "pet-store",
        "link": "https://petstore.swagger.io/v2/swagger.json"
    }, {
        "label": "WadeProject",
        "value": "wade-project",
        "link": "https://petstore.swagger.io/v2/swagger.json"
    }, {
        "label": "School API",
        "value": "school",
        "link": "https://petstore.swagger.io/v2/swagger.json"
    }]
    const [selectedOption, setSelectedOption] = useState(mockedOptions[0])

    function onOptionChange(newSelectedOption) {
        setSelectedOption(newSelectedOption);
        selectionHandler(newSelectedOption);
    }

    return (
        <Select
            selectedOption={selectedOption}
            options={mockedOptions}
            onChange={({detail}) => onOptionChange(detail.selectedOption)}
        />
    )
}
export default SelectApi;
