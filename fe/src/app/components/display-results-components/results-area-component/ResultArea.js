import React, { forwardRef, useEffect, useImperativeHandle, useState } from "react";
import ResultsAreaStyle from "./ResultArea.module.css";
import isEmpty from "lodash/isEmpty";
import RequestMessage from "../message-component/RequestMessage";
import ResponseMessage from "../message-component/ResponseMessage";

const ResultsArea = forwardRef((props, ref) => {
    const mockedResponse =
        '{"path":"this/is/your/path","responseBody":{\n' +
        '\t"random": 10,\n' +
        '\t"random float": 39.193,\n' +
        '\t"bool": false,\n' +
        '\t"date": "1999-04-23",\n' +
        '\t"regEx": "helloooooooooooo world",\n' +
        '\t"enum": "json",\n' +
        '\t"firstname": "Gerianna",\n' +
        '\t"lastname": "Voletta",\n' +
        '\t"city": "Puerto Williams",\n' +
        '\t"country": "United States Minor Outlying Islands",\n' +
        '\t"countryCode": "AL",\n' +
        '\t"email uses current data": "Gerianna.Voletta@gmail.com",\n' +
        '\t"email from expression": "Gerianna.Voletta@yopmail.com",\n' +
        '\t"array": [\n' +
        '\t\t"Agnese",\n' +
        '\t\t"Lily",\n' +
        '\t\t"Dania",\n' +
        '\t\t"Roberta",\n' +
        '\t\t"Yetty"\n' +
        "\t],\n" +
        '\t"array of objects": [\n' +
        "\t\t{\n" +
        '\t\t\t"index": 0,\n' +
        '\t\t\t"index start at 5": 5\n' +
        "\t\t},\n" +
        "\t\t{\n" +
        '\t\t\t"index": 1,\n' +
        '\t\t\t"index start at 5": 6\n' +
        "\t\t},\n" +
        "\t\t{\n" +
        '\t\t\t"index": 2,\n' +
        '\t\t\t"index start at 5": 7\n' +
        "\t\t}\n" +
        "\t],\n" +
        '\t"Aeriela": {\n' +
        '\t\t"age": 20\n' +
        "\t}\n" +
        "}}";
    const invalidMockedResponse = '{"error"}';
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        setMessages([...messages, props?.newRequest]);
    }, [props?.newRequest]);

    useImperativeHandle(ref, () => {
        return {
            setMessages: setMessages,
        };
    });

    return (
        <div className={ResultsAreaStyle.container}>
            {messages.map(
                (message) =>
                    !isEmpty(message.message) && [
                        message.isRequest ? (
                            <RequestMessage message={message.message} />
                        ) : (
                            <ResponseMessage message={message?.message} />
                        ),
                        <ResponseMessage message={mockedResponse} />,
                        <ResponseMessage message={invalidMockedResponse} />,
                    ]
            )}
        </div>
    );
});
export default ResultsArea;
