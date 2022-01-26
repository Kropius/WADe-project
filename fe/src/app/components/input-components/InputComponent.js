import React from "react";
import Box from "@awsui/components-react/box";
import Header from "@awsui/components-react/header";
import Container from "@awsui/components-react/container";
import SpaceBetween from "@awsui/components-react/space-between";
import Input from "@awsui/components-react/input";
import Button from "@awsui/components-react/button";
import Dictaphone from "./Dictatophone";
import {FormField, Spinner} from "@awsui/components-react";


const InputComponent = ({setNewRequest, isLoading}) => {
    const [value, setValue] = React.useState("");


    return (
        <Box>
            <Container header={<Header>Type/Record your request</Header>}>
                <SpaceBetween size="m">
                    <Input
                        value={value}
                        onChange={(event) => setValue(event.detail.value)}
                    />
                    <FormField>
                        <SpaceBetween size="m" direction="horizontal">
                            <Button variant="primary" onClick={() => setNewRequest({message: value, isRequest: true})}>
                                <SpaceBetween size={"m"} direction={"horizontal"}>
                                    <div>
                                        Get
                                    results
                                    </div>
                                    {isLoading ? <Spinner size={"normal"}/> : null}
                                </SpaceBetween>

                            </Button>
                            <Dictaphone handleInputChange={setValue} text="Talk"/>
                        </SpaceBetween>
                    </FormField>

                </SpaceBetween>
            </Container>
        </Box>
    );
};
export default InputComponent;
