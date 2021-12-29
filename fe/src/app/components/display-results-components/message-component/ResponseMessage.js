import React, {useEffect, useState} from "react";
import MessageStyle from "./Message.module.css";
import isEmpty from "lodash/isEmpty";
import JSONPretty from "react-json-pretty";
import JSONPrettyMon from "react-json-pretty/dist/monikai";

const ResponseMessage = ({message}) => {
    const [dataToBeDisplayed, setDataToBeDisplayed] = useState(null);

    useEffect(() => {
        try {
            setDataToBeDisplayed(JSON.parse(message));
            console.log(JSON.parse(message));
        } catch (e) {
            console.log(e);
            setDataToBeDisplayed(null);
        }
    }, [message])
    return ([
            !isEmpty(dataToBeDisplayed?.path) ?
                <code className={`${MessageStyle.bubble} ${MessageStyle.right}`}>{dataToBeDisplayed?.path}</code> :
                <code className={`${MessageStyle.bubble} ${MessageStyle.right} ${MessageStyle.invalid}`}>No path
                    provided</code>

            ,
            !isEmpty(dataToBeDisplayed?.responseBody) ?
                <div className={`${MessageStyle.bubble} ${MessageStyle.responseBody} ${MessageStyle.right}`}>
                    <JSONPretty data={dataToBeDisplayed?.responseBody} theme={JSONPrettyMon}></JSONPretty>
                </div> :
                <code className={`${MessageStyle.bubble} ${MessageStyle.right} ${MessageStyle.invalid}`}>No response
                    body
                    provided</code>
        ]

    )
};

export default ResponseMessage;
