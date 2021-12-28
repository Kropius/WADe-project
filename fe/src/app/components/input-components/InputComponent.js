import React from "react";
import Box from "@awsui/components-react/box";
import Header from "@awsui/components-react/header";
import Container from "@awsui/components-react/container";
import SpaceBetween from "@awsui/components-react/space-between";
import Input from "@awsui/components-react/input";
import Button from "@awsui/components-react/button";
import Dictaphone from "./Dictatophone";


const InputComponent = ({setNewRequest}) => {
    const [value, setValue] = React.useState("");
    return (
        <Box>
            <Container header={<Header>Type/Record your request</Header>}>
                <SpaceBetween size="m">
                    <Input
                        value={value}
                        onChange={(event) => setValue(event.detail.value)}
                    />
                    <SpaceBetween size="m" direction="horizontal">
                        <Button variant="primary" onClick={() => setNewRequest({message: value, isRequest: true})}>Get
                            results</Button>
                        <Dictaphone handleInputChange={setValue} text="Talk"/>
                    </SpaceBetween>
                </SpaceBetween>
            </Container>
        </Box>
    );
}
export default InputComponent;
