import React, {useState} from "react";
import {Select} from "@awsui/components-react";

// eslint-disable-next-line no-unused-vars
const SelectApi = ({options, selectionHandler}) => {

    const [selectedOption, setSelectedOption] = useState(null);

    function onOptionChange(newSelectedOption) {
        setSelectedOption(newSelectedOption);
        selectionHandler(newSelectedOption);
    }

    return (
        <Select
            selectedOption={selectedOption}
            options={options}
            onChange={({detail}) => onOptionChange(detail.selectedOption)}
        />
    );
};
export default SelectApi;
