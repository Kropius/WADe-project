import React, {useEffect, useState} from "react";
import MessageStyle from "./Message.module.css";
import isEmpty from "lodash/isEmpty";
import JSONPretty from "react-json-pretty";
import JSONPrettyMon from "react-json-pretty/dist/monikai";
import CallArea from "../CallArea";

const ResponseMessage = ({message}) => {
    const [requestData, setRequestData] = useState(null);
    const [requestBody, setRequestBody] = useState(null);

    useEffect(() => {
        setRequestBody(message?.request_body);
        const requestData = {
            path: message?.path ?? "N/A",
            verb: message?.verb ?? "N/A",
            queryParams: message?.query_params ?? "N/A"
        };
        setRequestData(requestData);
    }, [message]);
    return ([
                <div className={`${MessageStyle.bubble} ${MessageStyle.right} ${MessageStyle.requestBody}`}
                     key="requestData">
                    <JSONPretty data={requestData} theme={JSONPrettyMon}></JSONPretty>
                </div>,


                <div className={`${MessageStyle.bubble} ${MessageStyle.requestBody} ${MessageStyle.right}`}
                     key="requestBody">
                    <JSONPretty data={{requestBody: isEmpty(requestBody) ? "N/A" : requestBody}}
                                theme={JSONPrettyMon}></JSONPretty>
                </div>,
            <div className={`${MessageStyle.right}`}
                 key={`call-area-${requestBody}-${requestData}`}>
                <CallArea
                          />
            </div>


        ]

    );
};

export default ResponseMessage;
