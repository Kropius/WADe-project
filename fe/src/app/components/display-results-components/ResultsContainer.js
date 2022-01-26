import React, { useRef } from "react";
import { Container, SpaceBetween } from "@awsui/components-react";
import Header from "@awsui/components-react/header";
import ResultsArea from "./results-area-component/ResultArea";
import Button from "@awsui/components-react/button";

const ResultsContainer = ({ newRequest, setIsLoading }) => {
    const ref = useRef(null);
    const clearMessages = () => {
        ref.current.setMessages([]);
    };
    return (
        <Container
            header={
                <Header>
                    <SpaceBetween size={"xxl"} direction={"horizontal"}>
                        <div>Your results</div>
                        <Button onClick={clearMessages}>Clear</Button>
                    </SpaceBetween>
                </Header>
            }
        >
            <ResultsArea newRequest={newRequest} ref={ref} setIsLoading={setIsLoading}/>
        </Container>
    );
};

export default ResultsContainer;
