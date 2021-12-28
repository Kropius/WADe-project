import React from "react";
import {Button, SpaceBetween} from "@awsui/components-react";
import Icon from "@awsui/components-react/icon";

const UploadFile = () =>{
    return (
        <Button
            disabled={true}
            variant="primary"
            >
            <SpaceBetween size={"xs"} direction="horizontal">
                <Icon
                    variant = "normal"
                    name = "settings">
                </Icon>
                Upload File
            </SpaceBetween>

        </Button>
    )
}
export default UploadFile;
