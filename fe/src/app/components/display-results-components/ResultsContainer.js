import React from "react";
import {Container} from "@awsui/components-react";
import Header from "@awsui/components-react/header";
import ResultsArea from "./results-area-component/ResultArea";


const ResultsContainer = ({newRequest}) => {
    return (
        <Container header={<Header>Your results</Header>}>
            <ResultsArea newRequest={newRequest}/>

        </Container>
    )
}

export default ResultsContainer;
