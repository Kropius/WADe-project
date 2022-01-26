import React from "react";
import SwaggerUI from "swagger-ui-react";
import {Container} from "@awsui/components-react";
import SwaggerWidgetCSS from "./SwaggerWidget.module.css";
import Box from "@awsui/components-react/box";
import Header from "@awsui/components-react/header";

const SwaggerComponent = ({apiLink, title}) => {
    return (
        <Box>
            <Container header={<Header>{title}</Header>} className={SwaggerWidgetCSS.container}>

                <SwaggerUI url={apiLink}/>

            </Container>
        </Box>

    );

};
export default SwaggerComponent;
