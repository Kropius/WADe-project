import React, {useState} from "react";
import {Box, FormField, Icon, Modal, SpaceBetween, Spinner, Textarea} from "@awsui/components-react";
import Button from "@awsui/components-react/button";
import Input from "@awsui/components-react/input";
import isEmpty from "lodash/isEmpty";
import SpecificationApi from "../../../api/SpecificationApi";
import PubSub from "pubsub-js";
const UploadFile = () =>{
    const [visible, setVisible] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const [apiName, setApiName] = useState("");
    const [apiSpec, setApiSpec] = useState("");

    const [isValidOpenApiName, setIsValidOpenApiName] = useState(true);
    const [isValidOpenApiSpec, setIsValidOpenApiSpec] = useState(true);
    const showModal = () =>{
        setVisible(true);
    };

    function setOpenApiName(value){
        setIsValidOpenApiName(!isEmpty(value));
        setApiName(value);
    }

    function setOpenApiSpec(value){
        setIsValidOpenApiSpec(!isEmpty(value));

        setApiSpec(JSON.parse(JSON.stringify(value)));
        // console.log(JSON.parse(JSON.stringify(value).replace(/\\n/g, "")));
    }

    const  submitNewApi = async()=>{
        setIsLoading(true);
        await SpecificationApi().
        submitNewSpecification({id: apiName, open_api_specification: apiSpec})
            .then(() => {setIsLoading(false); PubSub.publish("success", "Successfully submitted, refresh the page");})
            .catch(() => {setIsLoading(false);});
    };
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
                            <Button variant="primary" onClick={submitNewApi}
                            disabled={isEmpty(apiSpec) || isEmpty(apiName) }>
                                <SpaceBetween size={"m"} direction={"horizontal"}>
                                    Upload specification
                                    {isLoading && <Spinner size={"normal"}/>}
                                </SpaceBetween></Button>
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
