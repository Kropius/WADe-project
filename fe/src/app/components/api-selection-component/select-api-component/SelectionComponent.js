import React from "react";
import {Box, SpaceBetween} from "@awsui/components-react";
import SelectApi from "./SelectApiComponent";
import UploadFile from "./UploadFileComponent";
import Header from "@awsui/components-react/header";
import Container from "@awsui/components-react/container";
import Grid from "@awsui/components-react/grid";

const SelectionComponent = ({handleApiSelection}) => {
    return (
        <div>
            <Container header={<Header>Select/Upload you api!</Header>}>
                <Grid gridDefinition={[{colspan: 6}, {colspan: 6}]}
                      direction="horizontal"
                >
                    <SelectApi selectionHandler={handleApiSelection}/>
                    <UploadFile/>
                </Grid>
            </Container>

        </div>
    )
}
export default SelectionComponent;
