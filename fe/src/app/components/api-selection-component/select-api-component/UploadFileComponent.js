import React, {useState} from "react";
import {Box, FormField, Icon, Modal, SpaceBetween, Textarea} from "@awsui/components-react";
import Button from "@awsui/components-react/button";
import Input from "@awsui/components-react/input";
import isEmpty from "lodash/isEmpty";
const UploadFile = () =>{
    const [visible, setVisible] = useState(false);

    const [apiName, setApiName] = useState("");
    const [apiSpec, setApiSpec] = useState("");

    const [isValidOpenApiName, setIsValidOpenApiName] = useState(true);
    const [isValidOpenApiSpec, setIsValidOpenApiSpec] = useState(true);

    const showModal = () =>{
        setVisible(true);
    };

    function setOpenApiName(value){
        if(!isEmpty(value)){
            setIsValidOpenApiName(true);}
        else{
            setIsValidOpenApiName(false);
        }
        setApiName(value);
    }

    function setOpenApiSpec(value){
        if(!isEmpty(value)){setIsValidOpenApiSpec(true);}
        else{
            setIsValidOpenApiSpec(false);
        }
        setApiSpec(value);
    }

    return ([
        <Button key="display-modal-button"
        onClick={showModal}>
            <SpaceBetween size={"xs"} direction="horizontal">
                <Icon
                    variant = "normal"
                    name = "settings">
                </Icon>
                Upload Specification
            </SpaceBetween>

        </Button>,
            <Modal
                key="upload-file-modal"
                onDismiss={()=>setVisible(false)}
                visible={visible}
                closeAriaLabel="Close modal"
                size="medium"
                footer={
                    <Box float="right">
                        <SpaceBetween direction="horizontal" size="xs">
                            <Button variant="link">Cancel</Button>
                            <Button variant="primary">Ok</Button>
                        </SpaceBetween>
                    </Box>
                }
                header="Upload specification"
            >

                    <SpaceBetween size={"m"}>
                        <FormField
                            label="Api name"
                        >
                        <Input
                            value={apiName}
                            onChange={({detail})=>setOpenApiName(detail.value)}
                            invalid={!isValidOpenApiName}
                        />
                        </FormField>
                        <FormField
                        label="Api Spec">
                        <Textarea
                            value={apiSpec}
                            onChange={({detail}) => setOpenApiSpec(detail.value)}
                            invalid = {!isValidOpenApiSpec}
                        />
                            </FormField>
                    </SpaceBetween>



            </Modal>
        ]

    );
};
export default UploadFile;
