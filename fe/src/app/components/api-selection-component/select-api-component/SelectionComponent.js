import React from "react";
import SelectApi from "./SelectApiComponent";
import UploadFile from "./UploadFileComponent";
import Header from "@awsui/components-react/header";
import Container from "@awsui/components-react/container";
import Grid from "@awsui/components-react/grid";
import Button from "@awsui/components-react/button";
import {SpaceBetween} from "@awsui/components-react";

// eslint-disable-next-line no-unused-vars
const SelectionComponent = ({options, handleApiSelection, loadSpecifications}) => {
    return (
        <Container header={<Header><SpaceBetween size={"m"} direction={"horizontal"}>Select/Upload you api!
            <Button iconAlign={"right"} iconName={"refresh"} onClick={loadSpecifications}>
                Refresh</Button></SpaceBetween> </Header>}>

            <Grid gridDefinition={[{colspan: 6}, {colspan: 6}]}
                  direction="horizontal"
            >
                <SelectApi selectionHandler={handleApiSelection} options={options}/>
                <UploadFile/>
            </Grid>
        </Container>


    );

};

export default SelectionComponent;
